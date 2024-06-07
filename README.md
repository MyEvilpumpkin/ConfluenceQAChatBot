# Confluence Knowledge Base Question Answering Bot

## About

This repository hosts an AI-powered chat application designed to provide information from a corporate knowledge base.

## Features

- **AI-Powered Chat**: Uses AI to answer questions based on corporate knowledge base materials.
- **Streamlit Integration**: Includes a Streamlit app for interactive chat.
- **Telegram Bot**: Implements a Telegram bot for chat functionality.

## Project Structure

```
root/
├── src/                             # Source code
│   ├── document_searching/          # Code related to document searching
│   ├── documents/                   # Code related to document handling
│   ├── preprocessing/               # Preprocessing scripts
│   ├── question_answering/          # Question answering system code
│   ├── streamlit_app/               # Streamlit app scripts
│   ├── telegram_bot/                # Telegram bot scripts
│   └── utils/                       # Utility scripts
│       ├── config.py                # Configuration handling
│       ├── loader.py                # General loaders
│       └── question_handler.py      # Handling questions logic
├── tests/                           # Test functionality
├── .gitignore                       # Git ignore file
├── README.md                        # Project documentation
├── requirements.txt                 # Python dependencies
├── start_streamlit_app.py           # Script to start the Streamlit app
└── start_telegram_bot.py            # Script to start the Telegram bot
```

## Usage

### 1. Install dependencies

To install the necessary dependencies, use:

```bash
pip install -r requirements.txt
```

### 2. Define document directories

To define document directories, use:

```bash
export DOCUMENT_DIRS=<dir1>:<dir2>:...:<dirN>
```

Each directory will be analyzed recursively

### 3a. Start Streamlit App

To start the Streamlit application, run:

```bash
python start_streamlit_app.py
```

### 3b. Start Telegram Bot

To start the Telegram bot, do next steps:

- Set up the Telegram bot token

```bash
export BOT_TOKEN=<your token>
```

- Launch Telegram bot

```bash
python start_telegram_bot.py
```

## Telegram bot usage

The bot can work in 2 modes:

1. Search for the most suitable document and search for the answer to the question in it  
To do this, you just need to write your question in a message to the bot

2. Search for several most suitable documents  
To do this you need to use the command  
```/top <number of documents in answer> <question>```
