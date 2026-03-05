#!/usr/bin/env python3
"""
Research engine for watchlist topics.
Searches web, Reddit, YouTube for specified topics.
"""
import os
import json
import time
import requests
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

# API Keys from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

class ResearchEngine:
    def __init__(self, db_path: str = "~/.openclaw/workspace/watchlist.db"):
        self.db_path = os.path.expanduser(db_path)
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                source TEXT NOT NULL,
                title TEXT,
                url TEXT,
                content TEXT,
                engagement INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                keywords TEXT,
                schedule_days INTEGER DEFAULT 7,
                last_run TIMESTAMP,
                enabled INTEGER DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def perplexity_search(self, query: str, days: int = 30) -> List[Dict]:
        """Search using Perplexity Sonar Pro via OpenRouter."""
        if not OPENROUTER_API_KEY:
            print("Warning: OPENROUTER_API_KEY not set")
            return []
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openclaw.ai",
            "X-Title": "Watchlist Research"
        }
        
        time_filter = f"Find trending discussions from the last {days} days about: {query}"
        
        data = {
            "model": "perplexity/sonar-pro",
            "messages": [
                {"role": "system", "content": "You are a research assistant. Find the most relevant and recent discussions, news, and updates. Include URLs when possible."},
                {"role": "user", "content": time_filter}
            ],
            "max_tokens": 4000,
            "temperature": 0.2
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=120)
            response.raise_for_status()
            result = response.json()
            
            content = result['choices'][0]['message']['content']
            findings = self._parse_findings(content, source="perplexity")
            return findings
            
        except Exception as e:
            print(f"Perplexity search error: {e}")
            return []
    
    def zhuk_search(self, query: str) -> List[Dict]:
        """Search using Zhuk deep research via OpenRouter."""
        if not OPENROUTER_API_KEY:
            return []
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "openrouter/alibaba/tongyi-deepresearch-30b-a3b",
            "messages": [
                {"role": "user", "content": f"Deep research: {query}. Find comprehensive sources with URLs."}
            ],
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=180)
            response.raise_for_status()
            result = response.json()
            
            content = result['choices'][0]['message']['content']
            findings = self._parse_findings(content, source="zhuk")
            return findings
            
        except Exception as e:
            print(f"Zhuk search error: {e}")
            return []
    
    def brave_search_for_tweets(self, query: str) -> str:
        """Use Brave search to find X/Twitter post URLs."""
        if not OPENROUTER_API_KEY:
            return ""
        
        # Use Perplexity to find specific X posts
        prompt = f"Find recent X/Twitter posts about '{query}' from the last 30 days. List the exact URLs and brief summaries."
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "perplexity/sonar-pro",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 3000
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except:
            return ""
    
    def reddit_search(self, query: str, limit: int = 25) -> List[Dict]:
        """Search Reddit for discussions."""
        try:
            url = "https://www.reddit.com/search.json"
            params = {
                "q": query,
                "sort": "new",
                "t": "month",
                "limit": limit
            }
            headers = {"User-Agent": "WatchlistResearch/1.0"}
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            findings = []
            for post in data.get("data", {}).get("children", []):
                p = post["data"]
                engagement = p.get("ups", 0) + p.get("num_comments", 0) * 2
                findings.append({
                    "title": p.get("title", ""),
                    "url": f"https://reddit.com{p.get('permalink', '')}",
                    "content": p.get("selftext", "")[:500],
                    "source": "reddit",
                    "engagement": engagement
                })
            
            return findings
            
        except Exception as e:
            print(f"Reddit search error: {e}")
            return []
    
    def youtube_search(self, query: str, days: int = 30) -> List[Dict]:
        """Search YouTube for videos."""
        try:
            # Use Invidious instance for search (no API key needed)
            instances = [
                "https://yt.lemnoslife.com",
                "https://invidious.snopyta.org",
                "https://vid.puffyan.us"
            ]
            
            findings = []
            for instance in instances:
                try:
                    url = f"{instance}/api/v1/search"
                    params = {
                        "q": query,
                        "sort_by": "date",
                        "type": "video",
                        "limit": 10
                    }
                    
                    response = requests.get(url, params=params, timeout=30)
                    if response.status_code == 200:
                        data = response.json()
                        for video in data[:10]:
                            findings.append({
                                "title": video.get("title", ""),
                                "url": f"https://youtube.com/watch?v={video.get('videoId', '')}",
                                "content": video.get("description", "")[:300],
                                "source": "youtube",
                                "engagement": video.get("viewCount", 0)
                            })
                        break
                except:
                    continue
            
            return findings
            
        except Exception as e:
            print(f"YouTube search error: {e}")
            return []
    
    def hn_search(self, query: str) -> List[Dict]:
        """Search Hacker News."""
        try:
            url = "https://hn.algolia.com/api/v1/search"
            params = {
                "query": query,
                "tags": "story",
                "hitsPerPage": 20
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            findings = []
            for hit in data.get("hits", []):
                findings.append({
                    "title": hit.get("title", ""),
                    "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    "content": hit.get("story_text", "")[:500] if hit.get("story_text") else "",
                    "source": "hackernews",
                    "engagement": hit.get("points", 0) + hit.get("num_comments", 0) * 2
                })
            
            return findings
            
        except Exception as e:
            print(f"HN search error: {e}")
            return []
    
    def _parse_findings(self, content: str, source: str) -> List[Dict]:
        """Parse LLM output into structured findings."""
        findings = []
        
        # Look for URLs
        url_pattern = r'https?://[^\s\)\]\>]+'
        urls = re.findall(url_pattern, content)
        
        # Split content into sections
        sections = re.split(r'\n\n+', content)
        
        for i, section in enumerate(sections):
            if len(section) > 50:  # Min length
                finding = {
                    "title": section.split('\n')[0][:200],
                    "url": urls[i] if i < len(urls) else "",
                    "content": section[:800],
                    "source": source,
                    "engagement": 0
                }
                findings.append(finding)
        
        return findings
    
    def research_topic(self, topic: str, days: int = 30) -> Dict:
        """Full research on a topic across all sources."""
        print(f"Researching: {topic}")
        
        all_findings = []
        
        # Run searches in parallel style (sequentially for now)
        print("  - Web search (Perplexity)...")
        perplexity_results = self.perplexity_search(topic, days)
        all_findings.extend(perplexity_results)
        time.sleep(1)
        
        print("  - Deep research (Zhuk)...")
        zhuk_results = self.zhuk_search(topic)
        all_findings.extend(zhuk_results)
        time.sleep(1)
        
        print("  - Reddit...")
        reddit_results = self.reddit_search(topic)
        all_findings.extend(reddit_results)
        time.sleep(1)
        
        print("  - YouTube...")
        youtube_results = self.youtube_search(topic)
        all_findings.extend(youtube_results)
        time.sleep(1)
        
        print("  - Hacker News...")
        hn_results = self.hn_search(topic)
        all_findings.extend(hn_results)
        time.sleep(1)
        
        print("  - Finding X posts...")
        x_content = self.brave_search_for_tweets(topic)
        if x_content:
            all_findings.append({
                "title": f"X/Twitter discussions about {topic}",
                "url": "",
                "content": x_content,
                "source": "x_twitter",
                "engagement": 0
            })
        
        # Sort by engagement
        all_findings.sort(key=lambda x: x.get("engagement", 0), reverse=True)
        
        # Store in database
        self._store_findings(topic, all_findings)
        
        return {
            "topic": topic,
            "findings": all_findings[:15],  # Top 15
            "total": len(all_findings),
            "timestamp": datetime.now().isoformat()
        }
    
    def _store_findings(self, topic: str, findings: List[Dict]):
        """Store findings in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for finding in findings:
            cursor.execute('''
                INSERT INTO findings (topic, source, title, url, content, engagement)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                topic,
                finding.get("source", "unknown"),
                finding.get("title", "")[:200],
                finding.get("url", "")[:500],
                finding.get("content", "")[:2000],
                finding.get("engagement", 0)
            ))
        
        cursor.execute('''
            UPDATE topics SET last_run = CURRENT_TIMESTAMP
            WHERE name = ?
        ''', (topic,))
        
        conn.commit()
        conn.close()
    
    def get_topic_history(self, topic: str, days: int = 7) -> List[Dict]:
        """Get historical findings for a topic."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM findings
            WHERE topic = ? AND found_at > datetime('now', '-{} days')
            ORDER BY found_at DESC
        '''.format(days), (topic,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            "id": r[0],
            "topic": r[1],
            "source": r[2],
            "title": r[3],
            "url": r[4],
            "content": r[5],
            "engagement": r[6],
            "found_at": r[8]
        } for r in rows]
    
    def get_all_topics(self) -> List[Dict]:
        """Get all configured topics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM topics WHERE enabled = 1')
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            "id": r[0],
            "name": r[1],
            "keywords": r[2],
            "schedule_days": r[3],
            "last_run": r[4]
        } for r in rows]

if __name__ == "__main__":
    engine = ResearchEngine()
    
    # Test
    result = engine.research_topic("OpenClaw new features")
    print(f"Found {result['total']} items")
    for f in result['findings'][:5]:
        print(f"- {f['title'][:80]}... ({f['source']})")
