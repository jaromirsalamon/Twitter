import datetime
import time
from datetime import date
import io

TEMPLATE = """{tweet_index}\t{tweet_id}\t{tweet_created}\t{tweet_expected}\t{tweet_sentiment}\t{tweet_user}\t{tweet_text}\n"""
TEMPLATE_CSV = """{tweet_index},{tweet_id},{tweet_created},{tweet_expected},{tweet_sentiment},{tweet_user},\"{tweet_text}\"\n"""
TEMPLATE_STAT = """{date}\ttotal: {total}\tpositive: {positive}\tnegative: {negative}\tpos/neg ratio: {ratio}\n"""
TEMPLATE_STAT_CSV = """{date},{total},{positive},{negative},{ratio}\n"""
t = ['07:30:00', '08:15:00', '09:00:00', '09:45:00', '10:30:00', '11:15:00', '12:00:00', '12:45:00', '13:30:00', '14:15:00', '15:00:00', '15:45:00',
     '16:30:00', '17:15:00', '18:00:00', '18:45:00', '19:30:00', '20:15:00', '21:00:00', '21:45:00', '22:30:00', '23:15:00', '23:59:59']

l = []
hash_tag = 'xpb'
for line in open('output/tweets-' + hash_tag + '-' + str(date.today()) + '.tsv', "rb").readlines():
    (tweet_id,tweet_created,tweet_user,tweet_text) = line.strip().split('\t')
    l.append({'tweet_id':tweet_id,'tweet_created':datetime.datetime.strptime(tweet_created, '%Y-%m-%d %H:%M:%S'),'tweet_user':tweet_user,'tweet_text':tweet_text})

tweet_index = 0
day_index = 1
prev_date = None
pos = 0
neg = 0
all = 0
day_counts = {}

out_file_name = 'output/tweets-extended-' + hash_tag + '-' + str(date.today()) + '.csv'
f = io.open(out_file_name, 'wb')

for item in l:
    t_index = 0

    actual_date = item['tweet_created'].date()

    if str(actual_date) in day_counts:
        day_counts[str(actual_date)]['all'] +=1
        day_counts[str(actual_date)]['pos'] = day_counts[str(actual_date)]['pos'] + 1 if ' #p ' in item['tweet_text'] else day_counts[str(actual_date)]['pos']
        day_counts[str(actual_date)]['neg'] = day_counts[str(actual_date)]['neg'] + 1 if ' #n ' in item['tweet_text'] else day_counts[str(actual_date)]['neg']
    else:
        day_counts[str(actual_date)] = {}
        day_counts[str(actual_date)]['all'] = 1
        day_counts[str(actual_date)]['pos'] = 1 if ' #p ' in item['tweet_text'] else 0
        day_counts[str(actual_date)]['neg'] = 1 if ' #n ' in item['tweet_text'] else 0


    if prev_date is None: prev_date = actual_date
    if (prev_date - actual_date).days != 0:
        prev_date = actual_date
        tweet_index = 0
        day_index += 1
        print
    tweet_index += 1

    for index in range(len(t)):
        epoch_plan = int(time.mktime(time.strptime(str(item['tweet_created'].date()) + ' ' + t[index], '%Y-%m-%d %H:%M:%S')))
        epoch_tweet = int(time.mktime(time.strptime(str(item['tweet_created'] + datetime.timedelta(hours=+2)), '%Y-%m-%d %H:%M:%S')))
        if (epoch_tweet - epoch_plan) < (45 * 60):
            t_index = index
            break

    if ' #p ' in item['tweet_text']:
        sentiment = 1
    elif ' #n ' in item['tweet_text']:
        sentiment = -1
    else:
        sentiment = 0

    f.write(TEMPLATE_CSV.format(tweet_index = '%02d' % tweet_index,
                          tweet_id = item['tweet_id'],
                          tweet_created = item['tweet_created'] + datetime.timedelta(hours=+2),
                          tweet_expected = str(item['tweet_created'].date()) + ' ' + t[t_index],
                          tweet_sentiment = sentiment,
                          tweet_user = item['tweet_user'],
                          tweet_text = item['tweet_text']
                          ))
f.close()

out_file_name = 'output/tweets-statistics-' + hash_tag + '-' + str(date.today()) + '.csv'
f = io.open(out_file_name, 'wb')

for key in sorted(day_counts.keys()):
    f.write(TEMPLATE_STAT_CSV.format(date = key,
                               total = ' %d' % day_counts[key]['all'],
                               positive = ' %d' % day_counts[key]['pos'],
                               negative = '  %d' % day_counts[key]['neg'],
                               ratio =  '{:.2f}'.format(day_counts[key]['pos'] * 1.00 / day_counts[key]['neg']) + '/1' if day_counts[key]['neg'] > 0 else 'N/A'
                          ))

    all += day_counts[key]['all']
    pos += day_counts[key]['pos']
    neg += day_counts[key]['neg']

f.write(TEMPLATE_STAT_CSV.format(date = '0000-00-00',
                           total = all,
                           positive = pos,
                           negative = neg,
                           ratio='{:.2f}'.format(pos * 1.00 / neg) + '/1'
                           ))

f.close()
print 'days: ' + str(day_index) + ', tweets per day (avg): ' + "{:.2f}".format(all * 1.00 / day_index)
