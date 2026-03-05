#!/usr/bin/env python3
"""
Watchlist management and research runner.
Usage: python3 watchlist.py <command> [args]
Commands:
  list              List all topics
  add <topic>       Add a new topic to watchlist
  run <topic|all>   Run research on topic(s)
  report [days]     Generate comprehensive report
  init              Initialize default topics
"""
import sys
import os

# Add script directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import sqlite3
from datetime import datetime, timedelta
from research_engine import ResearchEngine

# Default topics
DEFAULT_TOPICS = [
    {
        "name": "Peter Steinberger",
        "keywords": "Peter Steinberger, PSPDFKit, iOS development",
        "schedule_days": 30
    },
    {
        "name": "OpenClaw Features",
        "keywords": "OpenClaw, OpenClaw new features, OpenClaw updates, OpenClaw CLI",
        "schedule_days": 7
    },
    {
        "name": "IoT & Gadgets",
        "keywords": "IoT devices, new gadgets, smart home, embedded systems, sensors",
        "schedule_days": 7
    },
    {
        "name": "Startup Ideas",
        "keywords": "startup ideas, side projects, indie hackers, SaaS ideas, MVP",
        "schedule_days": 7
    },
    {
        "name": "B2B/B2C IoT Solutions",
        "keywords": "IoT B2B, IoT solutions, industrial IoT, smart devices business",
        "schedule_days": 7
    },
    {
        "name": "Business Problems for IoT",
        "keywords": "business problems, pain points, operational challenges, automation needs",
        "schedule_days": 7
    }
]

DB_PATH = os.path.expanduser("~/.openclaw/workspace/watchlist.db")

def init_db():
    """Initialize database with default topics."""
    engine = ResearchEngine()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for topic in DEFAULT_TOPICS:
        try:
            cursor.execute('''
                INSERT INTO topics (name, keywords, schedule_days)
                VALUES (?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    keywords = excluded.keywords,
                    schedule_days = excluded.schedule_days
            ''', (topic["name"], topic["keywords"], topic["schedule_days"]))
            print(f"  ✓ {topic['name']}")
        except Exception as e:
            print(f"  ✗ {topic['name']}: {e}")
    
    conn.commit()
    conn.close()
    print("\nTopics initialized!")

def list_topics():
    """List all topics."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, keywords, schedule_days, last_run, enabled
        FROM topics ORDER BY name
    ''')
    
    topics = cursor.fetchall()
    conn.close()
    
    if not topics:
        print("No topics configured. Run: watchlist.py init")
        return
    
    print("\n📋 Watchlist Topics:\n")
    for name, keywords, days, last_run, enabled in topics:
        status = "✓" if enabled else "✗"
        last = last_run.strftime('%Y-%m-%d %H:%M') if last_run else "Never"
        print(f"[{status}] {name}")
        print(f"    Keywords: {keywords[:60]}...")
        print(f"    Schedule: every {days} days | Last run: {last}\n")

def add_topic(name: str, keywords: str = "", days: int = 7):
    """Add a new topic."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO topics (name, keywords, schedule_days)
            VALUES (?, ?, ?)
        ''', (name, keywords or name, days))
        conn.commit()
        print(f"✓ Added: {name}")
    except sqlite3.IntegrityError:
        print(f"⚠ Topic already exists: {name}")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        conn.close()

def run_research(topic_name: str = "all", days: int = 30):
    """Run research on topic(s)."""
    engine = ResearchEngine()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if topic_name == "all":
        cursor.execute('SELECT name FROM topics WHERE enabled = 1')
        topics = [r[0] for r in cursor.fetchall()]
    else:
        cursor.execute('SELECT name FROM topics WHERE name LIKE ?', (f'%{topic_name}%',))
        topics = [r[0] for r in cursor.fetchall()]
        if not topics:
            topics = [topic_name]  # Single topic search
    
    conn.close()
    
    if not topics:
        print("No topics found. Add topics with: watchlist.py add <topic>")
        return
    
    results = []
    for topic in topics:
        print(f"\n🔍 Researching: {topic}")
        print("-" * 50)
        try:
            result = engine.research_topic(topic, days)
            results.append(result)
            print(f"\n✓ Found {result['total']} items about {topic}")
        except Exception as e:
            print(f"\n✗ Error researching {topic}: {e}")
    
    return results

def generate_report(days: int = 7):
    """Generate comprehensive report."""
    engine = ResearchEngine()
    
    print("\n" + "=" * 60)
    print("📊 WATCHLIST RESEARCH REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60 + "\n")
    
    topics = engine.get_all_topics()
    
    for topic in topics:
        findings = engine.get_topic_history(topic["name"], days)
        
        print(f"\n## {topic['name']}")
        print("-" * 40)
        print(f"Last run: {topic['last_run'] or 'Never'}")
        print(f"Findings (last {days} days): {len(findings)}")
        
        if findings:
            # Group by source
            by_source = {}
            for f in findings:
                src = f["source"]
                by_source[src] = by_source.get(src, []) + [f]
            
            print("\nTop findings:")
            for finding in findings[:5]:
                print(f"  • [{finding['source']}] {finding['title'][:70]}")
                if finding['url']:
                    print(f"    {finding['url'][:80]}")
    
    print("\n" + "=" * 60)
    print("End of Report")
    print("=" * 60 + "\n")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        init_db()
    elif command == "list":
        list_topics()
    elif command == "add":
        if len(sys.argv) < 3:
            print("Usage: watchlist.py add <topic> [keywords] [days]")
            sys.exit(1)
        name = sys.argv[2]
        keywords = sys.argv[3] if len(sys.argv) > 3 else name
        days = int(sys.argv[4]) if len(sys.argv) > 4 else 7
        add_topic(name, keywords, days)
    elif command == "run":
        if len(sys.argv) < 3:
            print("Usage: watchlist.py run <topic|all> [days]")
            sys.exit(1)
        topic = sys.argv[2]
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        run_research(topic, days)
    elif command == "report":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        generate_report(days)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
