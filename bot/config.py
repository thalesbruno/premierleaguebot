# config.py
import tweepy
import json
import logging

logger = logging.getLogger()


def create_api():

    with open('bot/credentials.json', 'r') as f:
        credentials = json.load(f)

        CONSUMER_KEY = credentials['consumer_key']
        CONSUMER_SECRET = credentials['consumer_secret']
        ACCESS_TOKEN = credentials['access_token']
        ACCESS_TOKEN_SECRET = credentials['access_token_secret']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e

    logger.info("API created")

    return api
