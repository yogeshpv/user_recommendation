#!/usr/bin/python
import ast
import json
import sys
import unicodedata

if len(sys.argv) < 2 :
  print 'Usage: {} <input_file>'.format(sys.argv[0])
  exit(1)

# Remove unicode characters from text
def remove_unicode(text_data):
    if text_data == None or text_data == '':
        return text_data
    return unicodedata.normalize('NFKD', text_data).encode('ascii','ignore')

def process_data():
	with open(sys.argv[1]) as tweet_file, open('processed_output.out','a') as tweet_out, \
				open('process_error.out','a') as error_log :
	    for counter, tweet in enumerate(tweet_file):
             try:
                if tweet[0] == '{' : # line starts as json and not error in stdout
                  tweet_info = (ast.literal_eval(tweet.strip()))
                  tweet_stored = dict()
                  if tweet_info['lang'] == 'en' : # English tweet
                      tweet_stored['id_str'] = tweet_info['id_str']
                      tweet_stored['truncated'] = tweet_info['truncated']
                      tweet_stored['created_at'] = tweet_info['created_at']
                      tweet_stored['favorited'] = tweet_info['favorited']
                      tweet_stored['favorite_count'] = tweet_info['favorite_count']
                      tweet_stored['retweet_count'] = tweet_info['retweet_count']
                      tweet_stored['retweeted'] = tweet_info['retweeted']
                      tweet_stored['geo'] = tweet_info['geo']
                      tweet_stored['user_id_str'] =  tweet_info['user']['id_str']
                      tweet_stored['user_screen_name'] = tweet_info['user']['screen_name']
                      tweet_stored['user_geo_enabled'] = tweet_info['user']['geo_enabled']
                      tweet_stored['user_followers_count'] = tweet_info['user']['followers_count']
                      tweet_stored['user_lang'] = tweet_info['user']['lang']
                      tweet_stored['user_statuses_count'] = tweet_info['user']['statuses_count']
                      tweet_stored['user_friends_count'] = tweet_info['user']['friends_count']
                      tweet_stored['user_description'] = remove_unicode(tweet_info['user']['description']) #removing unicode
                      tweet_stored['text'] = remove_unicode(tweet_info['text'])
                      tweet_stored['user_location'] = remove_unicode(tweet_info['user']['location'])
                      if tweet_info['place'] != None :
                          tweet_stored['place_country'] = remove_unicode(tweet_info['place']['country'])
                          tweet_stored['place_type'] = remove_unicode(tweet_info['place']['place_type'])
                          tweet_stored['place_bounding_box'] = tweet_info['place']['bounding_box']
                          tweet_stored['place_full_name'] = remove_unicode(tweet_info['place']['full_name'])

                      json.dump(tweet_stored, tweet_out, encoding = 'utf-8')
                      tweet_out.writelines('\n')
             except:
                error_log.writelines(sys.argv[1] + ': ' + str(counter) + ' Error: ' + str(sys.exc_info()[0]) + ' Tweet: ' + tweet)
                continue

if __name__ == "__main__":
   process_data() 
