import tweepy
from textblob import TextBlob
import pandas as pd
import re
# Step 1 - Authenticate
consumer_key= 'A8uQGb21KSstUMzxRqSrv8aMw'
consumer_secret= 'W44OBsZhR1VFZhFqCEyEbDGEgDFmif8R1afrkMRVFs136uy2CI'

access_token='2839876423-zwdU5iwHjy7Fb6cu5uPbR6WMt47boJaM5DaehDl'
access_token_secret='H5HBgk4WDvnIBsknMw0YzxSLI4RZKhumNjTKmrecLkSEB'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

query=raw_input('Enter a topic you want sentiments on: ')

public_tweets=api.search(query)

def get_label(analysis, threshold = 0):
	if analysis.sentiment[0]>threshold:
		return 'Positive'
	else:
		return 'Negative'

with open('tweets.csv', 'wb') as file:
	file.write('tweet,sentiment\n')
	for tweet in public_tweets:
		text=tweet.text.encode('utf-8')

		analysis = TextBlob(tweet.text)
		#Get the label corresponding to the sentiment analysis
		file.write('%s,%s\n' % (text, get_label(analysis)))

