
# ChatGPT Telegram Bot - README

## Overview

This is a Python-based Telegram bot that integrates OpenAI's GPT-3.5-turbo model to create an interactive chatbot. The bot allows users to interact with OpenAI's ChatGPT via Telegram, send queries, and receive responses. Additionally, it includes features like a referral system, premium subscription messaging, user profile tracking, and daily request limits.

## Features

- **OpenAI GPT-3.5 Integration**: Users can ask questions or request various tasks like writing, translating, coding, and more. 
- **Referral System**: Users can invite friends to the bot via a referral link and earn extra query requests.
- **Premium Subscription (Planned)**: The bot includes messaging about an upcoming premium subscription for additional benefits.
- **User Requests Management**: Each user gets a limited number of free queries daily, reset at a specified time.
- **Admin Stats Access**: The bot supports referral stats tracking for administrators.

## Prerequisites

- Python 3.7+
- A Telegram bot API token
- OpenAI API key
- Libraries:
  - `python-telegram-bot`
  - `openai`
  - `threading`
  - `time`

## Setup

### 1. Install Python Libraries

To install the required Python packages, run the following:

```bash
pip install python-telegram-bot openai
```

### 2. Obtain API Keys

- **Telegram API Token**: Register a bot with [BotFather](https://core.telegram.org/bots#botfather) on Telegram to get a bot token.
- **OpenAI API Key**: Obtain an API key by signing up for OpenAI’s services at [OpenAI API](https://beta.openai.com/).

### 3. Configuration

Replace the placeholder API keys in the script with your own in the `if __name__ == "__main__"` block:

```python
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAMBOT_APIKEY'
OPENAI_API_KEY = 'YOUR_OPENAI_APIKEY'
```

### 4. Run the Bot

Once configured, you can run the bot using the following command:

```bash
python chatgpt_telegram_bot.py
```

## Usage

### Commands

- **/start**: Start interacting with the bot.
- **/stats**: View referral statistics (available only to administrators).
- **User Commands**: Users can interact with the bot through text messages and buttons, such as:
  - Start a new dialogue
  - Check user profile
  - View referral link

### Key Features Breakdown

#### Referral System

Each user is assigned a unique referral link. When a new user joins via that link, the referring user earns extra query requests.

#### Daily Request Limit

Users are given a limited number of queries per day (set to 5 in this example). This limit resets daily at a specific time.

#### Loading Indicator

The bot simulates a "typing" or "loading" animation before sending responses, giving a more interactive user experience.

### Admin Features

Admins can view the referral statistics by using the `/stats` command, which provides an overview of the referral activity.

## Planned Features

- **Premium Subscription**: The bot includes placeholder code for a future premium subscription model that will allow users to bypass the daily request limit.
- **More Commands**: Add more commands like help, language switching, etc.

## Contributing

Feel free to open issues or submit pull requests for improvements or new features.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute it as needed.

---

This bot was developed as a way to integrate OpenAI's powerful language models into a Telegram-based conversational interface. Whether you're looking to use it as-is or build additional features, the code is designed to be extensible and straightforward to work with.
