from goToReddit import *
#from sendMail import *

after, before = oneDayAgo()
data = getPushshiftData(after,before)

#The length of data is the number submissions (data[0], data[1] etc),
#once it hits zero (after and before vars are the same) end
subCount = 0
print('where it started: ',after)
while True:#len(data)>0:
    for submission in data:
        collectSubData(submission)
        subCount+=1
    #print(str(datetime.fromtimestamp(data[-1]['created_utc'])))
    #update after variable to last created date of submission
    after = data[-1]['created_utc']
    #data has changed due to the new after variable provided by above code
    try:
        data = getPushshiftData(after, before)
    except json.decoder.JSONDecodeError:
        time.sleep(1)
        continue
    print(subCount)
    if len(data)==0:
        print('what it stopped at: ',after)
        print('after should equal before: ',before)
        print('total number of submissions: ',subCount)
        break

writeSubsFile()


#might be helpful
#use batch requests to speed up praw.
#pass it a list of fullnames to reddit.info instance
#https://github.com/Watchful1/Sketchpad/blob/master/postDownloader.py
