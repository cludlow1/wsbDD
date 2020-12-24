import praw

reddit = praw.Reddit("charles",user_agent = "charles_user_agent")
wsb = reddit.subreddit("wallstreetbets")

for post in wsb.hot(limit=10):
    print("#######################")
    print(post.title)
    print(post.score)
    print(post.id)
    print(post.url)
