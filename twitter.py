import tweepy
from credentials import Credentials
from datetime import date
from operator import itemgetter
import io

TEMPLATE_TSV = """{tweet_id}\t{tweet_created}\t{tweet_user}\t{tweet_text}\n"""
TEMPLATE_CSV = """{tweet_id},{tweet_created},{tweet_user},\"{tweet_text}\"\n"""

c = Credentials('config.json')

auth = tweepy.OAuthHandler(c.getConsumerKey(), c.getConsumerSecret())
auth.set_access_token(c.getAccessToken(), c.getAccessTokenSecret())

api = tweepy.API(auth)

l = []
hash_tag = 'xpb'
for tweet in tweepy.Cursor(api.user_timeline, screen_name=c.getScreenName()).items():
    if '#' + hash_tag in tweet.text:
        l.append({'tweet_id': tweet.id,
                  'tweet_created': tweet.created_at,
                  'tweet_user': tweet.user.screen_name.encode('UTF-8'),
                  'tweet_text': tweet.text.encode('UTF-8')
                  })

l = sorted(l, key=itemgetter('tweet_created'))

print(l[0:3])

out_file_name = 'output/tweets-' + hash_tag + '-' + str(date.today()) + '.csv'
print('Writing tweets to file: ' + out_file_name)
csv = io.open(out_file_name, 'wb')
out_file_name = 'output/tweets-' + hash_tag + '-' + str(date.today()) + '.tsv'
print('Writing tweets to file: ' + out_file_name)
tsv = io.open(out_file_name, 'wb')
for item in l:
    csv.write(TEMPLATE_CSV.format(tweet_id=item['tweet_id'],
                                       tweet_created=item['tweet_created'],
                                       tweet_user=item['tweet_user'],
                                       tweet_text=item['tweet_text']
                                       ))
    tsv.write(TEMPLATE_TSV.format(tweet_id=item['tweet_id'],
                                  tweet_created=item['tweet_created'],
                                  tweet_user=item['tweet_user'],
                                  tweet_text=item['tweet_text']
                                  ))
csv.close()
tsv.close()
