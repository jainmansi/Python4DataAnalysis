
# coding: utf-8

# In[2]:

from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
import argparse
import json
from time import gmtime, strftime
import os
import glob


# In[9]:

#url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
API_KEY = 'slbBbLG1sh2hMg1MuIhk8fzNB'
API_SECRET = 'Cl59tZu1Rww9MB6lxq5qxyX6wFAm72DBEIsbVNZPWwzQnhwLat'
ACCESS_TOKEN = '4786768341-9KkLc5dn7qhIn220YeffLyLQJQlDr8EceB3Y7B0'
ACCESS_TOKEN_SECRET = 'ko0ELXDAJ1WJro6foeU7T5gjxE4c8340eeKjquXssVtFq'

auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#requests.get(url, auth=auth)

userIn = input("Enter topic you want to search:")

searchUrl = "https://api.twitter.com/1.1/search/tweets.json?lang=en&result_type=mix&count=1500&q=" + userIn;

r = requests.get(searchUrl, auth=auth, stream = True)

#print(type(r))
#for tweet in r.json():
    # print (tweet)
    
def new_folder(userIn):
    if not os.path.exists(userIn):
        os.makedirs(userIn)
        
for directory in os.listdir(): 
    if userIn!=directory:
        new_folder(userIn) 
                
fname = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
fname = userIn + "\\" + fname + '.json';

rec = dict(r.json())
json.dumps(rec)
with open(fname ,'w')as f:
    json.dump(rec, f)
P = json.load(open(fname))
print(P)


# In[10]:

from textblob import TextBlob

count = 0
positive = 0
negative = 0
neutral = 0

for filename in glob.glob(userIn + r"\*.json"):
    with open(filename, 'r') as f:
        P = json.load(f)

        for items in P["statuses"]:
    
            blob = TextBlob(items["text"])
            #print(items["text"])
    
            count += 1
            total = 0
    
            for sentence in blob.sentences:
                blob.tags
                blob.noun_phrases
                value = sentence.sentiment.polarity
                total += value
    
            if(total > 0):
                positive = positive + 1 
            elif total < 0:
                negative +=1
            else:
                neutral +=1
        
            #print(positive)
            #print(negative)
            #print(neutral)
            #print("total: {val}".format(val = total))

#print(count)
print("Out of total number of {val} tweets on the given topic, following results were obtained:".format(val = count))
print("{pos} percentage of people were postive,".format(pos = (positive/count)*100))
print("{neg} percentage of people were negative,".format(neg = (negative/count)*100))
print("{neu} percentage of people were neutral about this topic".format(neu = (neutral/count)*100))    


# In[121]:

import gmplot

count = 0
total = 0
tweets = []
for filename in glob.glob(userIn + r"\*.json"):
    with open(filename, 'r') as f:
        P = json.load(f)
        for items in P["statuses"]:
            try:
                #print(items["retweeted_status"]["place"])
                if(items["retweeted_status"]["user"]["verified"]):
                    tweets.append(items["text"])
            except KeyError:
                #print(items["place"])
                if(items["user"]["verified"]):
                    tweets.append(items["text"])

total = 0
for tweet in tweets:
    blob = TextBlob(tweet)
    
    for sentence in blob.sentences:
        blob.tags
        blob.noun_phrases
        value = sentence.sentiment.polarity
            
        total += value   

if(total > 0):
    outlook = "positive"
elif(total < 0):
    outlook = "negative"
else:
    outlook = "neutral"
    
print("For this topic, influential people with verified accounts tend to be more {val}".format(val = outlook))
                


# In[17]:

d = {}
d['Sun'] = d['Mon'] = d['Tue'] = d['Wed'] = d['Thu'] = d['Fri'] = d['Sat'] = 0

for filename in glob.glob(userIn + r"\*.json"):
    with open(filename, 'r') as f:
        P = json.load(f)

        for items in P["statuses"]:
            createdTime = items["created_at"]
            dateStr = "" + createdTime[0:3];
            d[dateStr] += 1

                  
sorted(d.values())
days = list(d.keys())
#print(days)
print("People talk more about this topic on :")
#print(d)
k = sorted(d, key=d.get, reverse=True)[:2]

print(k)


    


# In[93]:

favList = []

for filename in glob.glob(userIn + r"\*.json"):
    with open(filename, 'r') as f:
        P = json.load(f)
        
        for items in P["statuses"]:
            try:
                li = []
                retweeted_favourite_count = items['retweeted_status']['favorite_count']
                tweet = items["text"]
                li.append(retweeted_favourite_count)
                li.append(tweet)
                favList.append(li)
            except KeyError:
                retweeted_favourite_count = 0
                
temp = []
favList.sort(key=lambda x: x[0], reverse = True)
li = ['Total Count', 'Tweet'] 
item = []
item.append(li)
favList[0:0] = item
print("Most favorite tweet is:")
print(favList[1][1])
print("\n\"Open .csv file for more detailed summary\"")
import csv

import pyexcel
pyexcel.save_as(array = favList, dest_file_name = userIn + r'\MostFavoriteToLeastFavorite.csv')


# In[87]:

hashtagList = []

for filename in glob.glob(userIn + r"\*.json"):
    with open(filename, 'r') as f:
        P = json.load(f)

        for items in P["statuses"]:
            hashtagList.append(items["entities"]["hashtags"])
            
tagList = []
tagCount = {}
for items in hashtagList:
    for item in items:
        hashtag = "" + item["text"]
        hashtag = hashtag.lower()
        if hashtag not in tagCount:
            tagCount[hashtag] = 0
        else:
            tagCount[hashtag] += 1

k = sorted(tagCount, key=tagCount.get, reverse=True)[:3]
print("Top 3 hashtags for this topic are - {val}, {val2}, {val3}".format(val = k[0], val2 = k[1], val3 = k[2]))


# In[ ]:



