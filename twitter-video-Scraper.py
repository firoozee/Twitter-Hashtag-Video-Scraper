import pandas as pd
import tweepy
import pytz
import datetime
import time
#generated file name will be the same as date

# Set up Twitter API credentials
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'access_token'
access_secret = 'access_secret'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)

# Define search query and date range
search_query = "#MahsaAmini"
#change the date from here
since_date = datetime.datetime(2023, 3, 22, tzinfo=pytz.UTC)
until_date = since_date + datetime.timedelta(days=1)

# Define list to store tweets
tweets = []

# Define variables for pagination hey MK;) for the first try keep the max_tweets at a low num to see if it runs proprly and u get the excel output
# for the first run change the sleep time to 10 sec
max_tweets = 10000000
tweets_per_query = 100

# Search for tweets
for i in range(0, max_tweets // tweets_per_query):
    query = f"{search_query} since:{since_date.strftime('%Y-%m-%d')} until:{until_date.strftime('%Y-%m-%d')} -filter:retweets filter:videos"
    search_results = api.search_tweets(q=query, lang="en", tweet_mode="extended", count=tweets_per_query, result_type="recent")
    tweets += search_results

    # Print progress
    print(f"{len(tweets)} tweets captured")

    # Sleep for 1 minute after every 100 requests see the Twitter api Rules for requests per min, change 60 for trial
    if i % 100 == 0:
        print("Waiting for 1 minute...")
        time.sleep(60)

# Convert tweets to Pandas DataFrame
df = pd.DataFrame([{
    "user": tweet.user.screen_name,
    "url": f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}",
    "date": tweet.created_at
} for tweet in tweets])

# Create Excel file name based on search query and date range
excel_file = f"{search_query[1:]}-hashtags-{since_date.date()}.xlsx"

# Write data to Excel file
df.to_excel(excel_file, index=False)

print(f"Total {len(tweets)} tweets captured and saved to {excel_file}")
