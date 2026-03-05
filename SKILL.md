---
name: watchlist-research
description: IoT, gadgets, and startup research watchlist. Monitors topics via web search, Reddit, YouTube, and X. Use when: researching IoT devices, B2B/B2C problems solvable by IoT, startup ideas, gadget reviews, Peter Steinberger updates, OpenClaw new features, or any watchlist-based recurring research. Triggers onwatchlist management, /watchlist command, or research report requests.
---

# Watchlist Research Skill

A research tool for monitoring IoT, gadgets, startups, and technology topics continuously.

## Capabilities

- **Web Search**: Uses Perplexity Sonar Pro via OpenRouter and Zhuk for comprehensive web search
- **Reddit Analysis**: Finds trending discussions and community sentiment
- **YouTube Analysis**: Discovers videos and transcripts on topics
- **X/Twitter Search**: Tracks posts and discussions (requires API key/service)
- **Watchlist**: Persistent tracking of topics with scheduling
- **Reports**: Generates comprehensive reports with citations

## Topics Monitored

1. **Peter Steinberger** - Follow updates every 30 days
2. **OpenClaw Features** - New features and capabilities
3. **IoT & Gadgets** - New IoT devices and tech innovations
4. **Startup Ideas** - Business ideas to implement
5. **B2B/B2C IoT Solutions** - Gadgets solving business problems
6. **Business Problems** - Opportunities for IoT commercial products

## Commands

### Add to Watchlist
```
watchlist add "topic"
watchlist add "Peter Steinberger" every 30 days
```

### Run Research
```
watchlist run all
watchlist run "topic name"
```

### Generate Report
```
watchlist report
```

## Usage

Invoke with `$watchlist` or command `/watchlist`.

## API Keys Required

- `OPENROUTER_API_KEY` - For Perplexity Sonar Pro web search
- `OPENAI_API_KEY` - For text processing

Optional:
- `X_API_KEY` - For X/Twitter search via API service
- `BRAVE_API_KEY` - Alternative web search backend

## Scripts

- `scripts/watchlist.py` - Main watchlist management and research
- `scripts/research_engine.py` - Research engine with web search
- `scripts/references/watchlist_topics.md` - Watchlist configuration

## See Also

- [Watchlist Topics](references/watchlist_topics.md) - Configured topics
- [Research Sources](references/research_sources.md) - Available data sources
