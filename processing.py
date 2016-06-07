import codecs
import datetime

TEMPLATE = """{tweet_index}\t{tweet_id}\t{tweet_created}\t{tweet_user}\t{tweet_text}"""
TEMPLATE_STAT = """{date}\ttotal: {total}\tpositive: {positive}\tnegative: {negative}\tpos/neg ratio: {ratio}"""
t = ['07:30', '08:15', '09:00', '09:45', '10:30', '11:15', '12:00', '12:45', '13:30', '14:15', '15:00', '15:45',
     '16:30', '17:15', '18:00', '18:45', '19:30', '20:15', '21:00', '21:45', '22:30', '23:15', '00:00']

l = []
for line in open('output/tweets-2016-06-07.csv', "rb").readlines():
    (tweet_id,tweet_created,tweet_user,tweet_text) = line.strip().split('\t')
    l.append({'tweet_id':tweet_id,'tweet_created':datetime.datetime.strptime(tweet_created, '%Y-%m-%d %H:%M:%S'),'tweet_user':tweet_user,'tweet_text':tweet_text})

tweet_index = 0
day_index = 1
prev_date = None
pos = 0
neg = 0
all = 0
day_counts = {}

for item in l:

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

    print(TEMPLATE.format(tweet_index = '%02d' % tweet_index,
                          tweet_id = item['tweet_id'],
                          tweet_created = item['tweet_created'] + datetime.timedelta(hours=+2),
                          tweet_user = item['tweet_user'],
                          tweet_text = item['tweet_text']
                          ))

for key in sorted(day_counts.keys()):
    print(TEMPLATE_STAT.format(date = key,
                               total = ' %d' % day_counts[key]['all'],
                               positive = ' %d' % day_counts[key]['pos'],
                               negative = '  %d' % day_counts[key]['neg'],
                               ratio =  '{:.2f}'.format(day_counts[key]['pos'] * 1.00 / day_counts[key]['neg']) + '/1' if day_counts[key]['neg'] > 0 else 'N/A'
                          ))

    all += day_counts[key]['all']
    pos += day_counts[key]['pos']
    neg += day_counts[key]['neg']

print(TEMPLATE_STAT.format(date = '0000-00-00',
                           total = all,
                           positive = pos,
                           negative = neg,
                           ratio='{:.2f}'.format(pos * 1.00 / neg) + '/1'
                           ))
print 'days: ' + str(day_index) + ', tweets per day (avg): ' + "{:.2f}".format(all * 1.00 / day_index)
