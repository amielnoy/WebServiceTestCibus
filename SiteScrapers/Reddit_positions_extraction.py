import praw
import pandas as pd

reddit_read_only = praw.Reddit(client_id="H63JO2m7ZIzkI8_C8ncwsw",  # your client id
                               client_secret="a4cyRGklRw6MqIYhA_-vzUWu28WXTw",  # your client secret
                               user_agent="amielnoy")  # your user agent

subreddit = reddit_read_only.subreddit("redditdev")

# Display the name of the Subreddit
print("Display Name:", subreddit.display_name)

# Display the title of the Subreddit
print("Title:", subreddit.title)

# Display the description of the Subreddit
print("Description:", subreddit.description)
# extract the 5 hotest posts from redit
subreddit = reddit_read_only.subreddit("Python")

# print("5 hotest redit post titles")
# for post in subreddit.hot(limit=5):
#     print("*****redit post title*****")
#     print(post.title)
#     print()

top_posts = subreddit.top(time_filter="week")

print("Get Last week posts text")
# Print the text of the top post
print()
print()
for post in top_posts:
    print("****************************This is the begging of top post************************************")
    print(post.selftext)
    print("****************************This is the End of top post************************************")
    print("*******************************************************************************************")
    print("*******************************************************************************************")