import urllib
from datetime import datetime
import datetime
import urllib.request
import praw


# from praw.models.listing.mixins import subreddit

class redditExtraction:
    @staticmethod
    def get_reddit_top_week_posts_titles():
        reddit_read_only = praw.Reddit(client_id="H63JO2m7ZIzkI8_C8ncwsw",  # your client id
                                       client_secret="a4cyRGklRw6MqIYhA_-vzUWu28WXTw",  # your client secret
                                       user_agent="amielnoy")  # your user agent

        subreddit = reddit_read_only.subreddit("redditdev")
        titles_result_list = []
        # Display the name of the Subreddit
        print("Display Name:", subreddit.display_name)
        titles_result_list.append(subreddit.display_name)
        # Display the title of the Subreddit
        print("Title:", subreddit.title)
        titles_result_list.append(subreddit.title)
        # Display the description of the Subreddit
        print("Description:", subreddit.description)
        titles_result_list.append(subreddit.description)
        return titles_result_list

    @staticmethod
    def print_and_get_last_week_posts_text():
        reddit_read_only = praw.Reddit(client_id="H63JO2m7ZIzkI8_C8ncwsw",  # your client id
                                       client_secret="a4cyRGklRw6MqIYhA_-vzUWu28WXTw",  # your client secret
                                       user_agent="amielnoy")  # your user agent

        # extract the 5 hotest posts from redit
        subreddit = reddit_read_only.subreddit("Python")

        print("5 hotest redit post titles")
        for post in subreddit.hot(limit=5):
            print("*****redit post title*****")
            print(post.title)
            print()

        top_posts = subreddit.top(time_filter="week")

        print("Get Last week posts text")
        # Print the text of the top post
        print()
        print()
        result_title_list = []
        for post in top_posts:
            print("****************************This is the begging of top post************************************")
            print(post.selftext)
            print("****************************This is the End of top post************************************")
            print("*******************************************************************************************")
            print("*******************************************************************************************")
            result_title_list.append(post.selftext)
        return result_title_list
        # This code will download all the imagesfrom the top

    # posts of the 'funny'subreddit for the last week.
    # You can change the subreddit_name variable to the name of the subreddit you want to scrape, and modify the image download code to suit your needs.
    def get_images_of_Last_week_top_funny_posts():
        # Reddit API credentials
        reddit = praw.Reddit(client_id='your_client_id',
                             client_secret='your_client_secret',
                             user_agent='your_user_agent')

        # Subreddit name
        subreddit_name = 'funny'

        # Start and end timestamps for the past week
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=7)

        # Query the top posts for the past week
        from praw.models.listing.mixins import subreddit
        top_posts = reddit.subreddit(subreddit_name).top(limit=2)

        results_list = []
        # Loop through the top posts and download the images
        for post in top_posts:
            # Check if the post is an image
            if post.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
                # Check if the post was created within the past week
                if start_date.timestamp() <= post.created_utc <= end_date.timestamp():
                    # Download the image
                    image_url = post.url
                    image_name = f'{post.id}.{image_url.split(".")[-1]}'
                    urllib.request.urlretrieve(image_url, image_name)
                    results_list.append("image_name=" + image_name + "image_url=" + image_url)
        return results_list


# TODO fix images and there urls list
if __name__ == "__main__":
    # titles_result_list = redditExtraction.get_reddit_top_week_posts_titles()
    # print(titles_result_list)
    # posts_text_result_list = redditExtraction.print_and_get_last_week_posts_text()
    # print(posts_text_result_list)

     images_and_image_urls_list = redditExtraction.get_images_of_Last_week_top_funny_posts()
     print(images_and_image_urls_list)
