#!/usr/bin/python
import ast
import json
import sys
import unicodedata
import re

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


def cleanUpData():

    urls = '(?: %s)' % '|'.join("""http https www""".split())
    ltrs = r'\w'
    gunk = r'/#~:.?+=&%@!\-'
    punc = r'.:?\-'
    any = "%(ltrs)s%(gunk)s%(punc)s" % { 'ltrs' : ltrs,
                                         'gunk' : gunk,
                                         'punc' : punc }

    url = r"""
        \b                            # start at word boundary
            %(urls)s    :             # need resource and a colon
            [%(any)s]  +?             # followed by one or more of any valid character
        (?=                           # look-ahead non-consumptive assertion
                [%(punc)s]*           # either 0 or more punctuation
                (?:   [^%(any)s]      #  followed by a non-url char
                    |                 #   or end of the string
                      $
                )
        )
        """ % {'urls' : urls, 'any' : any, 'punc' : punc }

    url_re = re.compile(url, re.VERBOSE | re.MULTILINE)

    with open('processed_output.out') as tweet_file, open('processed_output_NEW.out','a') as tweet_out :
        for line in tweet_file.readlines():
            output = json.loads(line.strip())
            output['text'] = url_re.sub('', output['text'])
            output['text'] = re.sub('[^a-zA-Z@# ]+','', output['text'])
            json.dump(output, tweet_out, encoding = 'utf-8')
            tweet_out.writelines('\n')

if __name__ == "__main__":
   process_data()
   cleanUpData()


# with open('00.json') as f:
#     for row in f.readlines():
#         row_info = json.loads(row.strip())
#         try:
#             if row_info['lang'] == 'en' and row_info['place'] != None and \
#                             row_info['place']['bounding_box']['coordinates'][0][0][0] == float('-118.668404'):
#                 print row_info['place']
#                 eng_tweets.append(row_info)
#         except:
#             continue