import tweepy
import csv
import json

with open('twitter_credentials.json') as creds:
    info = json.load(creds)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']


def get_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    tweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    tweets.extend(new_tweets)

    oldest_tweet = tweets[-1].id - 1

    while len(new_tweets):
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest_tweet)
        tweets.extend(new_tweets)
        oldest_tweet = tweets[-1].id - 1
        print('...%s tweets have been downloaded so far' % len(tweets))

    out_tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode('utf-8')] for tweet in tweets]

    with open(screen_name + '_tweets.csv', 'w', encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'timestamp', 'message'])
        writer.writerows(out_tweets)


if __name__ == '__main__':
    get_tweets(input("Enter the handle to be monitored: "))
