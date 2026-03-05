# Watchlist Research Skill

AI-powered research tool for monitoring IoT, gadgets, startups, and technology topics.

## Features

- **Multi-source research**: Perplexity Sonar Pro, Zhuk, Reddit, YouTube, Hacker News
- **Scheduled monitoring**: Automatic research on configured topics
- **Persistent storage**: SQLite database for accumulating findings
- **Comprehensive reports**: Automated report generation

## Topics Monitored

1. **Peter Steinberger** - Every 30 days
2. **OpenClaw Features** - Weekly
3. **IoT & Gadgets** - Weekly
4. **Startup Ideas** - Weekly
5. **B2B/B2C IoT Solutions** - Weekly
6. **Business Problems** - Weekly

## Installation

```bash
# Clone skill
git clone https://github.com/jack-kholmogorov-bot/watchlist-research.git

# Install dependencies (use Homebrew Python on Linux/Mac)
pip3 install requests

# Setup environment
cp .env.example .env
# Edit .env and add your API keys

# Initialize topics
python3 scripts/watchlist.py init

# Run manually
python3 scripts/watchlist.py run all

# Setup cron (Tuesdays & Fridays at 8:00 AM)
./scripts/setup_cron.sh
```

## Cron Schedule

Runs automatically on:
- **Tuesday** at 8:00 AM
- **Friday** at 8:00 AM

## API Keys Required

| Service | Key | Purpose |
|---------|-----|---------|
| OpenRouter | `OPENROUTER_API_KEY` | Perplexity Sonar Pro + Zhuk search |
| OpenAI | `OPENAI_API_KEY` | Text processing |
| Brave (optional) | `BRAVE_API_KEY` | Alternative web search |

## X/Twitter Access

For searching X/Twitter posts, you have several options:

1. **X API v2** - Official, paid ($100+/month)
2. **RapidAPI Twitter** - Third-party, ~$20-50/month
3. **Browser cookies** - Free but manual (requires login)

The skill currently uses web search to find X posts (no direct API needed).

## YouTube Video Parsing

Uses Invidious API instances (no API key required) or yt-dlp for transcripts.

## Commands

```bash
# List all topics
python3 scripts/watchlist.py list

# Add custom topic
python3 scripts/watchlist.py add "Topic Name" "keywords"

# Run research on all topics
python3 scripts/watchlist.py run all

# Run on specific topic
python3 scripts/watchlist.py run "IoT & Gadgets"

# Generate report
python3 scripts/watchlist.py report
```

## Report Output

Reports include:
- Topic summaries
- Source breakdown (Reddit, X, YouTube, etc.)
- Top findings with engagement metrics
- Direct links to sources

## Automation

The skill is designed to work with OpenClaw heartbeat system and cron scheduling for fully automated research.
