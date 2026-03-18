# Ghostwriter Telegram Bot 🤖

A Telegram bot that acts as a personal ghostwriter. It takes a raw thought, cross-references it against a local database of past tweets to capture a specific "vibe," and uses the Gemini 2.5 Flash API to generate three distinct, publication-ready drafts.

## Tech Stack
* **Language:** Python 3.x
* **AI Provider:** Google Gemini API (`google-genai` SDK)
* **Interface:** Telegram API (`python-telegram-bot`)
* **Data Storage:** Local JSON

## Features
* **Vibe Engine Context:** Randomly pulls 5 historical tweets from a local JSON file to ground the LLM in the user's actual tone before generating new text.
* **Persona Generation:** Outputs three distinct variations of the thought:
  1. *The Builder* (Optimistic but frustrated)
  2. *The Raw Wisdom Speaker* (Casual, street-smart irony)
  3. *The Rational Doomer* (Sensationalist but logically sound)
* **Real-time Feedback:** Provides asynchronous feedback in Telegram so the user knows the AI is processing the request.

## Setup Instructions

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up Environment Variables**
Create a `.env` file in the root directory and add your API keys:
```
TELEGRAM_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_google_gemini_key_here
```

**4. Configure the Database**
Rename `vibe_db_sample.json` to `vibe_db.json` and replace the array strings with your own past content.

**5. Run the Bot**
```bash
python bot.py
```

## Usage
1. Start a chat with your bot on Telegram.
2. Send it a raw thought (e.g., "I am tired of fixing CSS bugs").
3. The bot will return the context it used and three drafted variations tailored to your defined personas.
