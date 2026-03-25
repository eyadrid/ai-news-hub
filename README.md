# AI News Aggregator

An intelligent news aggregation system that scrapes AI-related content from multiple sources (YouTube channels, RSS feeds), processes them with LLM-powered summarization, curates personalized digests based on user preferences, and delivers daily email summaries.

## Overview

This project aggregates AI news from multiple sources:

- **YouTube Channels**: Scrapes videos and transcripts from configured channels
- **RSS Feeds**: Monitors OpenAI and Anthropic blog posts
- **Processing**: Converts content to markdown, generates summaries, and creates digests
- **Curation**: Ranks articles by relevance to user profile using LLM
- **Delivery**: Sends personalized daily email digests

## Architecture

```mermaid
graph LR
    A[Sources<br/>YouTube<br/>RSS Feeds] --> B[Scrapers<br/>BaseScraper<br/>Registry Pattern]
    B --> C[(Database<br/>PostgreSQL)]
    C --> D[Processors<br/>Markdown<br/>Transcripts<br/>Digests]
    D --> C
    C --> E[Curator<br/>LLM Ranking]
    E --> F[Email<br/>Personalized Digest]
    F --> G[Delivery<br/>Gmail SMTP]

    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e8f5e9,stroke:#4caf50,stroke-width:3px
    style D fill:#fff4e1
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#ffe1f5
```

## How It Works

### Pipeline Flow

1. **Scraping** (`app/runner.py`)
   - Runs all registered scrapers
   - Fetches articles/videos from configured sources
   - Saves raw content to database

2. **Processing** (`app/services/process_*.py`)
   - **Anthropic**: Converts HTML articles to markdown
   - **YouTube**: Fetches video transcripts
   - **Digests**: Generates summaries using LLM

3. **Curation** (`app/services/process_curator.py`)
   - Ranks digests by relevance to user profile
   - Uses LLM to score and rank articles

4. **Email Generation** (`app/services/process_email.py`)
   - Creates personalized email digest
   - Selects top N articles
   - Generates introduction and formats content
   - Marks digests as sent to prevent duplicates

5. **Delivery** (`app/services/email.py`)
   - Sends HTML email via Gmail SMTP

### Daily Pipeline

The `run_daily_pipeline()` function orchestrates all steps:

- Ensures database tables exist
- Scrapes all sources
- Processes content (markdown, transcripts)
- Creates digests
- Sends email

## Project Structure

```
app/
├── agent/              # LLM agents for processing
│   ├── base.py        # Base agent class
│   ├── curator_agent.py   # Article ranking
│   ├── digest_agent.py    # Summary generation
│   └── email_agent.py     # Email content generation
├── config.py          # Configuration (YouTube channels)
├── database/          # Database layer
│   ├── models.py      # SQLAlchemy models
│   ├── repository.py # Data access layer
│   └── connection.py  # DB connection & environment
├── profiles/          # User profile configuration
│   └── user_profile.py
├── scrapers/          # Content scrapers
│   ├── base.py        # Base scraper for RSS feeds
│   ├── anthropic.py   # Anthropic RSS scraper
│   ├── openai.py      # OpenAI RSS scraper
│   └── youtube.py     # YouTube channel scraper
├── services/          # Processing services
│   ├── base.py        # Base process service
│   ├── process_anthropic.py
│   ├── process_youtube.py
│   ├── process_digest.py
│   ├── process_curator.py
│   ├── process_email.py
│   └── email.py       # Email sending
├── daily_runner.py    # Main pipeline orchestrator
└── runner.py          # Scraper registry & execution
```

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Groq API key
- Gmail app password (for email sending)

### Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   uv sync
   ```

3. Configure environment variables (create `.env`):

   ```bash
   DATABASE_URL=postgresql://user:pass@host:port/db

   # Email
   MY_EMAIL=your_email@gmail.com
   APP_PASSWORD=your_gmail_app_password

   # APIs
   GROQ_API_KEY=your_groq_key
   YOUTUBE_API_KEY=your_youtube_key
   ```

4. Initialize database:

   ```bash
   uv run setup_db.py
   ```

5. Configure YouTube channels in `app/config.py`

6. Update user profile in `app/profiles/user_profile.py`

### Running

**Full pipeline:**

```bash
uv run main.py 24 10
# Parameters: hours to scrape, top articles to digest
```

**Individual steps:**

```bash
# Scraping only
uv run app/runner.py

# Processing
uv run app/services/process_anthropic.py
uv run app/services/process_youtube.py
uv run app/services/process_digest.py

# Curation
uv run app/services/process_curator.py

# Email
uv run app/services/process_email.py
```

## Deployment

### GitHub Actions + Railway (Free)

**Prerequisites:**

- GitHub repository
- Railway account (free tier)
- API keys configured
- Gmail app password

**Setup:**

1. Create Railway PostgreSQL database
2. Add GitHub Secrets:
   - `DATABASE_URL` — Railway PostgreSQL connection string (public endpoint)
   - `MY_EMAIL` — Gmail address
   - `APP_PASSWORD` — Gmail app password
   - `GROQ_API_KEY` — Groq API key
   - `YOUTUBE_API_KEY` — YouTube API key

3. Push to GitHub → Workflow runs automatically daily at 9 AM UTC

4. Monitor:
   - GitHub Actions tab shows workflow status
   - Check email for daily digests
   - Railway dashboard shows database metrics

**Manual test:**

1. Go to GitHub repo → Actions
2. Click "Daily AI News Pipeline"
3. Click "Run workflow"
4. Check logs for execution details

## Key Features

- **Modular Architecture**: Base classes make it easy to extend
- **Scraper Registry**: Add new sources with minimal code
- **LLM-Powered**: Uses Groq for summarization and curation
- **Personalized**: User profile-based ranking
- **Duplicate Prevention**: Tracks sent digests
- **Multi-Source**: YouTube, RSS feeds, and more

## Technology Stack

- **Python 3.11+**: Core language
- **PostgreSQL**: Database
- **SQLAlchemy**: ORM
- **Pydantic**: Data validation
- **Groq API**: LLM processing
- **BeautifulSoup**: HTML parsing
- **feedparser**: RSS parsing
- **youtube-transcript-api**: Video transcripts
- **UV**: Package management
- **GitHub Actions**: Workflow automation
- **Railway**: PostgreSQL hosting

## Troubleshooting

### Database Connection Failed

- Verify DATABASE_URL uses **public** Railway endpoint (not internal)
- Check PostgreSQL service is running
- Confirm connection string format

### Email Not Sending

- Ensure APP_PASSWORD is exactly 16 characters (no spaces)
- Verify MY_EMAIL matches Gmail account password was generated for
- Check Gmail app password is created correctly

### API Rate Limits

- Groq free tier: ~30 requests/minute
- YouTube: Rate limited by API quota
- Reduce `hours` parameter if hitting limits

### Articles Not Scraping

- Verify API keys are correct
- Check RSS feed URLs are accessible
- Review logs for specific error messages

## Contributing

Feel free to:

- Add new news sources (create new scraper in `app/scrapers/`)
- Improve curation logic (modify agents)
- Suggest features via GitHub issues
- Improve documentation



**Status**: ✅ Production-ready | 🚀 Free deployment on Railway + GitHub Actions | 📅 Runs daily
