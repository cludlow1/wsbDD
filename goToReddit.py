import pandas as pd
import praw
import requests #Pushshift accesses Reddit via an url so this is needed
import json #JSON manipulation
import csv #To Convert final table into a csv file to save to your machine
import time
from datetime import datetime,timezone,timedelta
from dateutil.relativedelta import relativedelta

#allSubs is a global dictionary for all functions?
allSubs = {}

def usingPraw(postID):
    #as of right now im only interested in the score for a given post id
    #pushshift refuses to give me an accurate score but PRAW will
    reddit = praw.Reddit("charles",user_agent = "charles_user_agent")
    wsb = reddit.subreddit("wallstreetbets")
    post = reddit.submission(id=postID)
    return post.score

def oneDayAgo():
    before = int(time.time())
    dt = datetime.now()-relativedelta(days=1)
    after= int(dt.timestamp())
    #returns timestamps in UTC not EST
    return after,before

def getPushshiftData(after,before):
    #url = 'https://api.pushshift.io/reddit/search/submission/?size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str("wallstreetbets")
    url = 'https://api.pushshift.io/reddit/search/submission/?limit=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str("wallstreetbets")
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

#This function will be used to extract the key data points from each JSON result
def collectSubData(subm):
    #subData was created at the start to hold all the data which is then added to our global allSubs dictionary.
    subData = list() #list to store data points
    title = subm['title']
    url = subm['url']
    #flairs are not always present so we wrap in try/except
    try:
        flair = subm['link_flair_text']
    except KeyError:
        flair = "NaN"
    author = subm['author']
    sub_id = subm['id']
    score = subm['score']
    created = datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    numComms = subm['num_comments']
    permalink = subm['permalink']
    #Put all data points into a tuple and append to subData
    subData.append((sub_id,title,url,author,score,created,numComms,permalink,flair))
    #Create a dictionary entry of current submission data and store all data related to it
    allSubs[sub_id] = subData

def filterSubs(allSubs,sub):
    subStrToList = list(allSubs[sub][0])
    if subStrToList[8] == 'DD':
        return True
    else:
        return False

def writeSubsFile():
    with open("output.csv", 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Title","Url","Author","Score","Publish Date","Total No. of Comments","Permalink","Flair"]
        a.writerow(headers)
        for sub in allSubs:
            if filterSubs(allSubs,sub):
                correctScore = usingPraw(str(sub))
                tempList = list(allSubs[sub][0])
                tempList[4] = correctScore
                a.writerow(tuple(tempList))
            else:
                pass
