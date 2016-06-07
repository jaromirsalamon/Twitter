import tweepy
from credentials import Credentials
from datetime import date
from operator import itemgetter
import codecs
import io

TEMPLATE = """{tweet_id}\t{tweet_created}\t{tweet_user}\t{tweet_text}\n"""

c = Credentials('config.json')

auth = tweepy.OAuthHandler(c.getConsumerKey(), c.getConsumerSecret())
auth.set_access_token(c.getAccessToken(), c.getAccessTokenSecret())

api = tweepy.API(auth)

l = []
for tweet in tweepy.Cursor(api.user_timeline, screen_name='davidpiprof').items():
    if '#xfb' in tweet.text:
        l.append({'tweet_id': tweet.id,
                  'tweet_created': tweet.created_at,
                  'tweet_user': tweet.user.screen_name.encode('UTF-8'),
                  'tweet_text': tweet.text.encode('UTF-8')
                  })

l = sorted(l, key=itemgetter('tweet_created'))

out_file_name = 'output/tweets-' + str(date.today()) + '.csv'
print('Writing tweets to file: ' + out_file_name)
f = io.open(out_file_name, 'wb')
# fx = open('output/tweets-' + str(date.today()) + '.txt', "w")
for item in l:
    f.write(TEMPLATE.format(tweet_id=item['tweet_id'],
                                       tweet_created=item['tweet_created'],
                                       tweet_user=item['tweet_user'],
                                       tweet_text=item['tweet_text']
                                       ))
    # fx.write(item)

f.close()
# fx.close()
