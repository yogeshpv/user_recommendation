__author__ = 'veettily'
#!/usr/bin/python
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

def getting_firehose():
    SF_AREA = [-123.1512,37.0771,-121.3165,38.5396]
    NY_AREA = [-74.255735,40.496044,-73.700272,40.915256]
    LA_AREA = [-118.6682,33.7037,-118.1553,34.3373]
    CHICAGO = [-87.940267,41.644335,-87.524044,42.023131]

    AREA = SF_AREA

    l = StdOutListener()
    while True:
        try:
            stream = Stream(auth, l)
            stream.filter(locations = AREA)
        except:
            continue


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    getting_firehose()