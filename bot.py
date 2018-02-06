import os
import random
from os import listdir
from os.path import isfile, join
from time import strftime, localtime
import time

import markovify
import tweepy
from env import *

# ====== Individual bot configuration ==========================
bot_username = 'CorruptDex'
logfile_name = bot_username + ".log"


# ==============================================================

def get_value(model, chain_key):
    return model.chain.__dict__['model'][chain_key]


class Bot:
    def __init__(self):
        # Twitter authentication
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)

    def main(self):
        files = [f for f in listdir('./pokemon') if isfile(join('./pokemon', f))]
        with open('./corruptdex.txt', 'w') as outfile:
            for fname in files:
                with open('./pokemon/' + fname) as infile:
                    outfile.write(infile.read())

        with open('./corruptdex.txt') as f:
            text = f.read()

        text_model = markovify.Text(text)
        # text_model.get_value = get_value

        pokemon_names = map(lambda p: p.split('.')[0].split('-')[1].capitalize(), files)
        pokemon = random.choice(list(pokemon_names))
        tweeted = False
        while tweeted is False:
            pokemon_tweet = text_model.make_sentence_with_start(pokemon)
            if len(pokemon_tweet) < 140:
                print(pokemon_tweet)
                status = self.tweet(pokemon_tweet)
                first_tweet_id = status.id
                tweeted = True

                second_tweet_id = None
                it_tweet = text_model.make_sentence_with_start('It')
                if len(it_tweet) < 140:
                    second_tweet = self.tweet(it_tweet, first_tweet_id)
                    second_tweet_id = second_tweet.id
                    print(' ' + it_tweet)

                its_tweet = text_model.make_sentence_with_start('Its')
                if len(its_tweet) < 140:
                    if second_tweet_id is None:
                        self.tweet(its_tweet, first_tweet_id)
                        print(' ' + its_tweet)
                        print('first_tweet_id')
                        print(first_tweet_id)
                    else:
                        self.tweet(its_tweet, second_tweet_id)
                        print(' ' + its_tweet)
                        print('second_tweet_id')
                        print(second_tweet_id)

    def tweet(self, text, tweet_id=None):
        """Send out the text as a tweet."""

        # return self.api.user_timeline('CorruptDex')
        # Send the tweet and log success or failure
        try:
            if tweet_id is not None:
                status = self.api.update_status(text, tweet_id)
                self.log("Tweeted: " + text)
                time.sleep(2)
                return status
            else:
                status = self.api.update_status(text)
                self.log("Tweeted: " + text)
                time.sleep(2)
                return status

        except tweepy.error.TweepError as e:
            self.log(e.reason)

    def log(self, message):
        """Log message to logfile."""
        path = os.path.realpath(os.path.join(
            os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(path, logfile_name), 'a+') as f:
            t = strftime("%d %b %Y %H:%M:%S", localtime())
            f.write("\n" + t + " " + message)


if __name__ == "__main__":
    print()
    t = strftime("%d %b %Y %H:%M:%S", localtime())
    print('At: ' + t)
    Bot().main()
