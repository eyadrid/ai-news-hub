# Deployment Guide: GitHub Actions + Railway

This guide walks you through deploying the AI News Aggregator using GitHub Actions (free scheduling) and Railway (free PostgreSQL database).

## Step 1: Set up Railway PostgreSQL Database

### 1.1 Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (recommended) or email
3. Create a new project

### 1.2 Add PostgreSQL Plugin

1. Click "Add Service" → Select "PostgreSQL"
2. Railway will automatically create a database instance
3. Go to the PostgreSQL service and click "Connect"
4. Copy these values (you'll need them for GitHub Secrets):
   - **Host**: `xxx.railway.app` or IP address
   - **Port**: Usually `5432`
   - **Database**: `postgres` or custom name
   - **User**: `postgres` or custom user
   - **Password**: Generated password

### 1.3 Initialize Database Tables

Run this once to create tables:

```bash
# From your local machine (with .env configured):
python -c "from app.database.create_tables import create_all; create_all()"
```

Or in Railway shell:

```bash
python -c "from app.database.create_tables import create_all; create_all()"
```

---

## Step 2: Set up Gmail Authentication

Your app sends emails using Gmail's SMTP. You need an "App Password" (not your Gmail password).

### 2.1 Enable 2FA on Gmail

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click "Security" → Enable "2-Step Verification"

### 2.2 Generate App Password

1. Go to [Security Settings](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Windows Computer"
3. Copy the generated 16-character password
4. Save this as `APP_PASSWORD` secret in GitHub

---

## Step 3: Get API Keys

### 3.1 Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Create a new API key
4. Save as `GROQ_API_KEY` secret

### 3.2 YouTube API Key (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable YouTube Data API v3
4. Create an API key (Credentials → API key)
5. Save as `YOUTUBE_API_KEY` secret

---

## Step 4: Configure GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret" and add each:

| Secret Name         | Value                     |
| ------------------- | ------------------------- |
| `POSTGRES_USER`     | Railway postgres user     |
| `POSTGRES_PASSWORD` | Railway postgres password |
| `POSTGRES_HOST`     | Railway postgres host     |
| `POSTGRES_PORT`     | Railway postgres port     |
| `POSTGRES_DB`       | Database name             |
| `MY_EMAIL`          | Your Gmail address        |
| `APP_PASSWORD`      | Gmail app password        |
| `GROQ_API_KEY`      | Your Groq API key         |
| `YOUTUBE_API_KEY`   | YouTube API key           |

---

## Step 5: Configure & Test Workflow

### 5.1 Adjust Schedule (Optional)

Edit `.github/workflows/daily-pipeline.yml`:

```yaml
on:
  schedule:
    - cron: "0 9 * * *" # 9 AM UTC daily
```

**Cron format**: `minute hour day month weekday`

Examples:

- `0 8 * * *` - 8 AM UTC daily
- `0 9 * * 1-5` - 9 AM UTC weekdays only
- `30 18 * * *` - 6:30 PM UTC daily

### 5.2 Manual Test Run

1. Go to GitHub repo → Actions → "Daily AI News Pipeline"
2. Click "Run workflow" → "Run workflow"
3. Check the logs to verify it works

### 5.3 Debug Failed Runs

- Click the failed workflow
- Expand the "Run daily pipeline" step to see logs
- Check "Upload logs on failure" artifact for error details
- Common issues:
  - Database connection refused → Check POSTGRES_HOST and firewall
  - Email auth failed → Check APP_PASSWORD doesn't have spaces
  - API key invalid → Confirm key is copied correctly (no extra spaces)

---

## Step 6: Monitor & Maintain

### 6.1 View Past Runs

- GitHub repo → Actions → "Daily AI News Pipeline"
- Click any workflow to see logs and duration

### 6.2 Check Railway Database

- Log in to Railway
- Your PostgreSQL service shows:
  - Data usage
  - Connections
  - Logs
  - Pricing (should be free tier)

### 6.3 Change Schedule

- Edit `.github/workflows/daily-pipeline.yml`
- Commit and push changes
- Next schedule will use new cron

---

## Important Notes

### Costs

- **GitHub Actions**: FREE for public repos, 2,000 free minutes/month for private repos (plenty for once-daily runs)
- **Railway PostgreSQL**: FREE tier ($5/month trial credit)
- **Groq API**: FREE with rate limits (~120 requests/day)
- **Gmail**: FREE to send

### Limitations

- GitHub Actions workflow can run up to 35 days late if offline
- Railway free tier sleeps after 7 days of inactivity (restart on next request)
- Ensure database connection stays active

### Troubleshooting

**Database connection refused:**

```
Error: could not connect to server
```

- Check Railway PostgreSQL is running
- Verify POSTGRES_HOST matches Railway settings
- Check firewall allows your IP (Railway handles this)

**Gmail authentication failed:**

```
SMTPAuthenticationError: Invalid credentials
```

- Don't use regular Gmail password
- Use 16-character app password
- Verify MY_EMAIL matches the account the password was generated for

**Groq API rate limited:**

```
RateLimitError
```

- Free tier has limits (~30 requests/minute)
- Reduce top_n or hours parameters in main.py

---

## Next Steps

1. ✅ Create Railway PostgreSQL database
2. ✅ Generate Gmail app password
3. ✅ Get API keys (Groq, YouTube)
4. ✅ Add all secrets to GitHub
5. ✅ Test workflow manually
6. ✅ Monitor first few runs
7. 🎉 Automated daily digests!

For issues, check:

- GitHub Actions logs (repo → Actions)
- Railway database logs (Railway console)
- Application error messages in workflow output
