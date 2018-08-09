#!/usr/bin/env python

import sys

def output(fo, tweet_id, user_id, timestamp, body):
    if '\"' in body:
        print body
        body = body.replace('\"', '')
        print body
    fo.write('%s,%s,%s,%s\n' % (tweet_id, user_id, timestamp, body.replace('\t', '\\t')))

def process(src, dst):
    tweet_id = ''
    user_id = ''
    timestamp = ''
    body = ''

    #fo = open(dst, 'w')

    n = 0
    for line in open(src):
        n += 1
        line = line.rstrip('\r\n')
        fields = line.split('\x01')
        if len(fields) >= 4:
            body = body.replace('\"', '')
            if tweet_id:
                output(fo, tweet_id, user_id, timestamp, body)
            tweet_id = fields[0]
            user_id = fields[1]
            timestamp = fields[2]
            body = '\x01'.join(fields[3:])
        else:
            body += '\\n' + line

    if tweet_id:
        output(fo, tweet_id, user_id, timestamp, body)

if __name__ == '__main__':
    dst = sys.argv[1] + '.txt'
    fo = open(dst, 'w')
    fo.write('tweet_id, user_id, timestamp, body\n')
    for src in sys.argv[1:]:
        dst = src + '.csv'
        print "converting: %s to %s" % (src, dst)
        process(src, dst)
