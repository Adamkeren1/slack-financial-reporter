# Slack Financial Reporter - Implementation Plan

## Overview
Build an automated agent that sends USD/ILS exchange rate and BTC/USD price to a Slack channel every business day when the market is open.

---

## Phase 1: Setup & Prerequisites

### 1.1 Slack App Configuration
- ✅ Create Slack app at https://api.slack.com/apps
- ✅ Add OAuth scopes: `chat:write`, `chat:write.public`, `channels:read`
- ✅ Install app to workspace
- ✅ Obtain Bot Token (starts with `xoxb-`)
- ✅ Note the Channel ID for target channel

### 1.2 Local Environment Setup
- Install Python 3.8+ 
- Install required packages: `slack-sdk`, `requests`, `python-dotenv`, `schedule`
- Create `.env` file with credentials
- Test Slack connection

---

## Phase 2: Project Structure

```
slack-financial-reporter/
├── .env                          # Environment variables (IGNORED in git)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── config.py                     # Configuration management
├── financial_reporter.py         # Main agent script
├── market_utils.py               # Market hours checker
├── slack_utils.py                # Slack API wrapper
├── scheduler.py                  # Scheduling logic
├── README.md                     # Setup & usage guide
└── logs/                         # Log files directory
```

---

## Phase 3: Core Components

### 3.1 Market Hours Detection
- **Function**: `is_market_open()`
- **Logic**: Check if current time is during US market hours (9:30 AM - 4:00 PM ET, Monday-Friday)
- **Handles**: US holidays, timezone conversions

### 3.2 Data Fetching
- **USD/ILS Rate**: Use free API (e.g., exchangerate-api.com, CoinGecko)
- **BTC/USD Price**: Use CoinGecko API (free, no key required)
- **Error Handling**: Retry logic + fallback values

### 3.3 Slack Integration
- **Library**: `slack-sdk` (official Python client)
- **Method**: `client.chat_postMessage()` to send formatted messages
- **Features**: 
  - Formatted message blocks
  - Error notifications
  - Rate limiting handling

### 3.4 Scheduling
- **Library**: `schedule` or system cron/Task Scheduler
- **Frequency**: Once daily at market open (9:30 AM ET)
- **Fallback**: System-level scheduler for reliability

---

## Phase 4: Implementation Steps

### Step 1: Create Environment File
```bash
# .env
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_CHANNEL_ID=C1234ABCD
TIMEZONE=America/New_York
MESSAGE_TIME=09:30
```

### Step 2: Install Dependencies
```bash
pip install slack-sdk requests python-dotenv schedule pytz
```

### Step 3: Implement Core Modules
- `config.py` - Load and validate env variables
- `market_utils.py` - Timezone & market hours logic
- `slack_utils.py` - Slack API wrapper functions
- `financial_reporter.py` - Main execution logic

### Step 4: Test Locally
```bash
python financial_reporter.py
# Should send test message to Slack
```

### Step 5: Set Up Scheduling
- **Windows**: Task Scheduler (automated batch file runner)
- **Linux/Mac**: cron job (`crontab -e`)
- **Cloud**: AWS Lambda, Google Cloud Functions, or Heroku

---

## Phase 5: Deployment Options

### Option A: Local Machine (Windows Task Scheduler)
1. Create batch script that runs Python
2. Set up Task Scheduler to run daily at 9:30 AM ET
3. Requires machine to be on

### Option B: Cloud (AWS Lambda / Google Cloud Functions)
1. Deploy code to cloud function
2. Use CloudWatch Events / Pub/Sub for scheduling
3. No local machine needed

### Option C: Heroku / VPS
1. Deploy app with persistent scheduler
2. Reliable, runs 24/7
3. Low cost for simple tasks

---

## Phase 6: Message Format

**Example message to Slack:**
```
📊 Daily Market Update - August 16, 2026

🇺🇸 USD / ILS: 3.65
₿ BTC / USD: $42,350

Market Status: OPEN ✅
Next update: Tomorrow 9:30 AM ET
```

---

## Phase 7: Error Handling & Monitoring

- Try/catch blocks for API calls
- Log all events to `logs/` directory
- Slack notifications for errors
- Email alerts for critical failures (optional)
- Retry logic for failed API calls (3 attempts)

---

## Phase 8: Testing Checklist

- [ ] Slack connection test
- [ ] Market hours detection test
- [ ] Exchange rate API test
- [ ] BTC price API test
- [ ] Message formatting test
- [ ] Scheduler test (runs at correct time)
- [ ] Error handling test (simulate API failure)
- [ ] Timezone handling test
- [ ] Holiday detection test

---

## Estimated Timeline

| Phase | Time |
|-------|------|
| Setup & Config | 15 min |
| Core Implementation | 45 min |
| Testing | 30 min |
| Deployment Setup | 20 min |
| **Total** | **~2 hours** |

---

## Resources

- [Slack API Docs](https://api.slack.com/methods/chat.postMessage)
- [ExchangeRate API](https://exchangerate-api.com)
- [CoinGecko API](https://www.coingecko.com/en/api)
- [Python Schedule Library](https://schedule.readthedocs.io/)
- [Pytz Timezone Docs](https://pypi.org/project/pytz/)

---

## Security Notes

- Never commit `.env` file to git
- Rotate tokens if accidentally exposed
- Use environment variables, not hardcoded values
- Implement rate limiting for Slack API
- Log sensitive operations (without logging tokens)

