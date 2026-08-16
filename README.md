# Slack Financial Reporter

An automated agent that sends daily USD/ILS exchange rates and BTC/USD prices to your Slack channel every business day when the market is open.

## Features

✅ **Automated Daily Updates** - Sends messages at market open (9:30 AM ET)  
✅ **Market Hours Aware** - Only sends during US market open hours (9:30 AM - 4:00 PM ET)  
✅ **Weekend & Holiday Detection** - Skips weekends and US market holidays  
✅ **Multiple Deployment Options** - Windows Task Scheduler, cron, cloud functions, or always-on server  
✅ **Error Handling** - Retry logic and comprehensive logging  
✅ **Free APIs** - Uses free, publicly available APIs (no paid subscriptions required)  
✅ **Formatted Messages** - Rich Slack formatting with blocks  

## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Slack workspace and bot token (see [Getting Your Slack Token](PLAN.md#step-by-step-generate-slack-bot-token))
- Your target Slack channel ID

### Installation

1. **Clone/Set Up the Project**
   ```bash
   cd slack-financial-reporter
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your values:
   # SLACK_BOT_TOKEN=xoxb-your-token-here
   # SLACK_CHANNEL_ID=C1234ABCD
   # TIMEZONE=America/New_York
   # MESSAGE_TIME=09:30
   ```

   **How to get these values:**
   - `SLACK_BOT_TOKEN`: From https://api.slack.com/apps → Your App → OAuth & Permissions → Bot User OAuth Token (starts with `xoxb-`)
   - `SLACK_CHANNEL_ID`: Right-click channel in Slack → "Copy link" → Extract ID from URL (e.g., `C1234ABCD`)

### Testing

1. **Test Slack Connection**
   ```bash
   python slack_utils.py
   ```
   Expected output: `✅ Connected to Slack as: U1234ABCD`

2. **Test Financial APIs**
   ```bash
   python financial_api.py
   ```
   Expected output: Shows current USD/ILS and BTC/USD rates

3. **Test Full Reporter**
   ```bash
   python financial_reporter.py
   ```
   This will send a test message to your Slack channel if the market is open.

4. **Test Market Utils**
   ```bash
   python market_utils.py
   ```
   Shows current market status and timezone info.

## Running the Reporter

### Option 1: Manual Execution
```bash
python financial_reporter.py
```

### Option 2: Python Scheduler (Not Recommended for Production)
```bash
python scheduler.py
```
This runs continuously and checks every minute if it's time to send the message. Not ideal for long-term use.

### Option 3: Windows Task Scheduler (Recommended for Windows)

1. **Create a Batch File** (`run_reporter.bat`)
   ```batch
   @echo off
   cd /d "C:\Users\adamk\repos\slack-financial reporter"
   venv\Scripts\python.exe financial_reporter.py
   ```

2. **Open Task Scheduler**
   - Press `Win + R` → Type `taskschd.msc` → Enter

3. **Create a New Task**
   - Click "Create Basic Task" in right panel
   - Name: "Slack Financial Reporter"
   - Description: "Send daily market updates to Slack"
   - Click Next

4. **Set Trigger**
   - Select "Daily"
   - Start time: 9:30 AM (or your preferred time)
   - Recurrence: Every 1 day
   - Click Next

5. **Set Action**
   - Select "Start a program"
   - Program: `C:\Users\adamk\repos\slack-financial reporter\run_reporter.bat`
   - Click Next → Finish

6. **Test the Task**
   - Right-click the task → Run
   - Check Slack channel for message

### Option 4: Linux/macOS Cron Job

1. **Edit Crontab**
   ```bash
   crontab -e
   ```

2. **Add Cron Entry** (9:30 AM ET, Monday-Friday)
   ```cron
   30 09 * * 1-5 cd /home/user/slack-financial-reporter && /usr/bin/python3 financial_reporter.py
   ```

3. **Verify Cron Job**
   ```bash
   crontab -l
   ```

### Option 5: Cloud Deployment (AWS Lambda / Google Cloud Functions)

1. **Prepare Function Code**
   - Combine all Python files into a single handler function
   - Create `requirements.txt` with dependencies

2. **Deploy to AWS Lambda**
   - Create new function
   - Upload code as ZIP
   - Set environment variables
   - Create CloudWatch Events trigger (9:30 AM daily)

3. **Deploy to Google Cloud Functions**
   - Create new function
   - Set runtime to Python 3.9+
   - Deploy with Cloud Scheduler trigger

## Project Structure

```
slack-financial-reporter/
├── financial_reporter.py      # Main script - run this daily
├── financial_api.py           # Financial data fetching logic
├── slack_utils.py             # Slack API integration
├── market_utils.py            # Market hours & timezone utilities
├── scheduler.py               # Python-based scheduler (alternative)
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (DO NOT COMMIT)
├── .env.example              # Template for .env file
├── .gitignore                # Git ignore rules
├── PLAN.md                   # Detailed implementation plan
└── logs/                     # Log files directory
    └── financial_reporter.log
```

## Configuration

Edit `.env` file to customize:

```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_CHANNEL_ID=C1234ABCD

# Market Settings
TIMEZONE=America/New_York              # Your timezone (use pytz timezone names)
MESSAGE_TIME=09:30                     # Time to send message (24-hour format)

# Logging
LOG_LEVEL=INFO                         # INFO, DEBUG, WARNING, ERROR
```

### Available Timezones
Some common options:
- `America/New_York` - Eastern Time (Market default)
- `America/Chicago` - Central Time
- `America/Denver` - Mountain Time
- `America/Los_Angeles` - Pacific Time
- `Europe/London` - London
- `Europe/Paris` - Central European Time
- `Asia/Tokyo` - Japan

Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## Logs

All activities are logged to `logs/financial_reporter.log`. View recent logs:

```bash
# View last 50 lines
tail -n 50 logs/financial_reporter.log

# View entire log
cat logs/financial_reporter.log
```

## Troubleshooting

### "Missing required configuration" Error
**Solution:** Make sure `.env` file exists and contains `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID`

### "Slack connection failed" Error
**Solution:** 
- Verify token is correct and starts with `xoxb-`
- Check token hasn't been revoked at https://api.slack.com/apps
- Ensure bot has `chat:write` permission

### "Market is not open" (No message sent)
**Solution:**
- This is normal! Market only sends during 9:30 AM - 4:00 PM ET on weekdays
- Test during market hours or modify `MESSAGE_TIME` to current time

### "Failed to fetch exchange rate" Error
**Solution:**
- Check internet connection
- ExchangeRate API might be down - try again later
- Log file shows exact API error

### "Invalid timezone" Error
**Solution:**
- Check `TIMEZONE` in `.env` uses valid pytz timezone name
- See "Available Timezones" section above

## Message Format

The bot sends formatted messages like this:

```
📊 Daily Market Update

🇺🇸 USD / ILS
3.6500

₿ BTC / USD
$42,350.00

Market Status: ✅ OPEN
Next update: Tomorrow 9:30 AM ET
```

## Security

⚠️ **Important Security Notes:**

1. **Never commit `.env` file** - It's in `.gitignore` for a reason!
2. **Keep your token secret** - If exposed, regenerate it immediately
3. **Use environment variables** - Don't hardcode secrets in code
4. **Rotate tokens periodically** - Best practice for API security

## APIs Used

### ExchangeRate API
- **URL:** https://api.exchangerate-api.com
- **Free:** Yes (up to 1500 requests/month)
- **Data:** Currency exchange rates
- **No authentication required** for basic usage

### CoinGecko API
- **URL:** https://api.coingecko.com
- **Free:** Yes (unlimited)
- **Data:** Cryptocurrency prices
- **No authentication required**

## Support & Issues

If you encounter issues:

1. **Check the logs:** `logs/financial_reporter.log`
2. **Verify configuration:** All required `.env` variables present
3. **Test components individually:**
   ```bash
   python config.py          # Check config
   python market_utils.py    # Check market hours
   python financial_api.py   # Check API calls
   python slack_utils.py     # Check Slack connection
   python financial_reporter.py  # Full test
   ```

## Advanced Customization

### Modify Message Format
Edit the `create_market_update_blocks()` method in [slack_utils.py](slack_utils.py#L67)

### Add More Financial Metrics
Add new methods to [financial_api.py](financial_api.py) to fetch additional data (stocks, commodities, etc.)

### Change Market Hours
Modify `MARKET_OPEN_HOUR` and `MARKET_CLOSE_HOUR` in [config.py](config.py#L47)

### Add More Currencies/Cryptos
Update `get_all_rates()` in [financial_api.py](financial_api.py#L70)

## Future Enhancements

- [ ] Add support for multiple channels
- [ ] Custom message templates per channel
- [ ] Store historical data for trend analysis
- [ ] Add interactive buttons for more details
- [ ] Multi-currency support
- [ ] Database integration for historical tracking
- [ ] Web dashboard for viewing updates
- [ ] Email notifications as fallback

## License

MIT License - Feel free to use and modify for your needs

## Credits

- [Slack API Python SDK](https://github.com/slackapi/python-slack-sdk)
- [ExchangeRate API](https://exchangerate-api.com)
- [CoinGecko API](https://www.coingecko.com/api)

---

**Happy trading! 📈**
