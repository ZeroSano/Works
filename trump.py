# -*- coding: utf-8 -*-
# In[]:
from twitter import *
import time
import sys
import pandas as pd
from pymongo import MongoClient

# In[]:
t = Twitter(auth=OAuth(
        '3580970233-H86yQ7rKIpbHCyHkOitJ2aFXqxeCplAjCwthl6L',
        'sWsVxL7nJ3vjAsYuV8OWTgGt35cp3DPFuarooa4cz6ahE',
        'quXFzAou9W24n2SY1XUuoxWuZ',
        'eqEqxj1QuCP3jR5brdkcgGYH3MdUQARTJr1hirIvfqQa52195l',
    ))
"""
t = Twitter(auth=OAuth(
        access_token_key='3580970233-H86yQ7rKIpbHCyHkOitJ2aFXqxeCplAjCwthl6L',
        access_token_secret='sWsVxL7nJ3vjAsYuV8OWTgGt35cp3DPFuarooa4cz6ahE'
        consumer_key='quXFzAou9W24n2SY1XUuoxWuZ'
        consumer_secret='eqEqxj1QuCP3jR5brdkcgGYH3MdUQARTJr1hirIvfqQa52195l'
    ))
"""

# In[]:
# get tweet
GO = True
datetime, twt, rts = [], [], []
# latest tweet ID (2:48 PM - 2 July 2018)
max_id = 1013902140409040897
# 38.1K, from March 2009
collection = 38000
count = 200
while GO:
    try:
        TimeLine = t.statuses.user_timeline(user_id = 25073877, count=count, max_id=max_id, exclude_replies = True, include_rts = True)
        for tweet in TimeLine:
            twt.append(tweet['text'])
            datetime.append(tweet['created_at'])
            if tweet['text'][0] + tweet['text'][1] + tweet['text'][2] == 'RT ':
                rts.append(True)
            else:
                rts.append(False)
        max_id = TimeLine[-1]['id']-1
        time.sleep(500)
        print ('{:2f} % complete.'.format(len(twt)/collection))
        if len(twt)+1 > collection:
            print('finished searching.')
            GO = False
    except Exception as e:
        print ('type:' + str(type(e)) )
        print ('message:' + e.message )
        sys.exit()

# In[]:
# to to_csv
df = pd.DataFrame({'Datetime': datetime, 'Tweet': twt, 'RT': rts})
# df.to_csv('trumpTweet.csv')   # df to csv

# In[]:
# to_db
client = MongoClient('localhost', 27017)
db = client.tweet
tw = db.trumpTweet
for _, row in df.iterrows():
    tw.insert_one(
        {
            'Datetime': row.Datetime,
            'Tweet': row.Tweet,
            'RT': row.RT
        }
    )
