import logging
import logging.handlers
from table import get_table
import json
from config import create_api
import time
import tweepy

# Setting log configurations
LOG_FILE = 'bot/pl_bot.log'
FORMAT = logging.Formatter(
    '%(asctime)-15s %(name)-8s %(levelname)-8s %(message)s')
logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(
    LOG_FILE, maxBytes=10000000, backupCount=5)
handler.setFormatter(FORMAT)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# Creating tweepy API
try:
    api = create_api()
    logger.info(f"API created")
except Exception as e:
    logger.error(f"Error creating API: {e}")


def check_mentions(since_id):
    """
    Function that check mentions and reply with some PL content according with
    keyword mentioned in the user tweet
    """
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if any(k in tweet.text.lower() for k in ['tabela', 'table']):
            logger.info(f"Sending PL table to {tweet.user.name}")
            pl_table = get_table()
            try:
                api.update_status(
                    f"@{tweet.user.screen_name} {pl_table}", in_reply_to_status_id=tweet.id)
            except Exception as e:
                logger.error(f"Error updating status: {e}")
    return new_since_id


def main():
    with open('bot/last_since_id.json', 'r') as f:
        last_since_id = json.load(f)
    since_id = int(last_since_id['last_since_id'])
    while True:
        since_id = check_mentions(since_id)
        with open('bot/last_since_id.json', 'w') as f:
            try:
                json.dump({'last_since_id': str(since_id)}, f)
            except Exception as e:
                logger.error(f"Error writing last since id: {e}")
        time.sleep(60)


if __name__ == "__main__":
    main()
