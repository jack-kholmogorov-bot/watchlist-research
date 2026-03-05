# Research Sources

## Web Search (Primary)

### OpenRouter -> Perplexity Sonar Pro
- **URL**: https://openrouter.ai/api/v1/chat/completions
- **Model**: perplexity/sonar-pro
- **Cost**: ~$0.0025 per 1M tokens
- **Features**: Real-time web search with citations

### OpenRouter -> Zhuk (Deep Research)
- **URL**: https://openrouter.ai/api/v1/chat/completions
- **Model**: openrouter/alibaba/tongyi-deepresearch-30b-a3b
- **Features**: Deep research with web search

### Brave Search (Free Tier)
- **URL**: https://api.search.brave.com/res/v1/web/search
- **Free Tier**: 2,000 queries/month
- **Features**: Web search with AI summarization

## X/Twitter (Posts)

### Options for X Search:

1. **Scraping with browser cookies** (Free, requires browser auth)
   - Use browser automation
   - Requires user to be logged into x.com

2. **X API v2** (Paid)
   - **Basic**: $100/month, 10K tweets/month
   - **Pro**: $5,000/month, 1M tweets/month
   - **URL**: https://api.twitter.com/2/

3. **Third-party APIs**:
   - **RapidAPI Twitter API**: ~$20-50/month
   - **Tweetscout**: Various pricing tiers

4. **Nitter** (Free, unofficial, unreliable)

## Reddit

### Radit API
- **URL**: https://www.reddit.com/search.json
- **Free with rate limits**
- **Features**: Search posts, comments, subreddits

### Pushshift API
- **URL**: https://api.pushshift.io/reddit/search/submission/
- **Features**: Historical search, better rate limits

## YouTube

### YouTube Data API v3
- **Free Tier**: 10,000 quota units/day (approx 50-100 searches)
- **URL**: https://www.googleapis.com/youtube/v3/
- **Features**: Search, video details, transcripts (with yt-dlp)

### yt-dlp
- **Command**: `yt-dlp --extract-metadata --write-sub`
- **Features**: Download videos, extract metadata, subtitles

## Hacker News

### HN Search API
- **URL**: https://hn.algolia.com/api/v1/search
- **Free, no API key required**
- **Features**: Search stories, comments, polls

## Polymarket (Prediction Markets)
- **URL**: https://api.polymarket.com/
- **Features**: Track prediction markets on topics
