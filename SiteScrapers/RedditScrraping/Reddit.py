import praw

def get_reddit_posts():
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

    top_posts = subreddit.top(time_filter="day")

    print("Get Last week posts text")
    # Print the text of the top post
    print()
    print()
    res = []
    # return top 5 posts
    for post in top_posts:
        print("****************************This is the begging of top post************************************")
        print(post.selftext)
        print(post.subreddit.display_name + ',' + post.subreddit.advertiser_category  + ',' + post.author.fullname + ',' + str(post.author.total_karma) + ',' + str(post.score) + post.title + ',' + str(post.ups)+ ',' + str(post.upvote_ratio) + post.selftext + ',' + post.thumbnail + post.domain + str(post.created))
        res.append({
            'subreddit': post.subreddit.display_name,
            'advertiser_category': post.subreddit.advertiser_category,
            'author': post.author.fullname,
            'total_karma': post.author.total_karma,
            'score': post.score,
            'title': post.title,
            'ups': post.ups,
            'upvote_ratio': post.upvote_ratio,
            'selftext': post.selftext,
            'thumbnail': post.thumbnail,
            'domain': post.domain,
            'created': post.created

        })

        print("****************************This is the End of top post************************************")
        print("*******************************************************************************************")
        print("*******************************************************************************************")
    return res