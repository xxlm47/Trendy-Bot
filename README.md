# Trendy-Bot

A Telegram bot that fetches trending topics from Reddit.

## Setup

1.  **Get a Telegram Bot Token:**
    *   Talk to the [BotFather](https://t.me/botfather) on Telegram.
    *   Create a new bot by sending the `/newbot` command.
    *   Follow the instructions and BotFather will give you a token. Keep this token secure!

2.  **Configure the Bot:**
    *   Open the `main.py` file.
    *   Find the line `TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN_HERE'`.
    *   Replace `'YOUR_TELEGRAM_BOT_TOKEN_HERE'` with the actual token you received from BotFather.

3.  **Install Dependencies:**
    *   Ensure you have Python 3 and pip (Python package installer) installed.
    *   Install the required Python packages by running the following command in the root directory of the project:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Configure Reddit API Access (for `reddit_scraper.py`):**
    *   The `reddit_scraper.py` script uses PRAW (Python Reddit API Wrapper) to fetch data from Reddit.
    *   You need to configure PRAW with your Reddit API credentials. The script expects a `praw.ini` file in the same directory, or for environment variables to be set.
    *   Create a `praw.ini` file in the root of the project with your Reddit app's `client_id`, `client_secret`, and `user_agent`. Example:
        ```ini
        [bot1]
        client_id=YOUR_CLIENT_ID
        client_secret=YOUR_CLIENT_SECRET
        user_agent=YOUR_USER_AGENT by /u/YOUR_REDDIT_USERNAME
        ```
    *   Alternatively, set the environment variables: `PRAW_CLIENT_ID`, `PRAW_CLIENT_SECRET`, `PRAW_USER_AGENT`.
    *   For more details on PRAW configuration, refer to the [PRAW documentation](https://praw.readthedocs.io/en/stable/getting_started/configuration.html).

## Running the Bot

1.  Ensure you have configured your Telegram bot token in `main.py` and Reddit API access via `praw.ini` or environment variables.
2.  Run the bot using:
    ```bash
    python main.py
    ```
3.  Interact with your bot on Telegram. Send `/start` to see if it's online and `/run reddit` to fetch Reddit trends.
