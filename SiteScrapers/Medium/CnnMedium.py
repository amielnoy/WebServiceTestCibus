import requests
from bs4 import BeautifulSoup


class MediumScrraper:

    @staticmethod
    def getPostsFullText():
        url = 'https://medium.com/@mythiliraju651/best-15-test-automation-trends-for-2023-75108209696f'
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the post text elements
        post_text_elements = soup.find_all("p")

        # Extract and concatenate the text from the post text elements
        post_text = ""
        for element in post_text_elements:
            post_text += element.text.strip() + " "
        print(post_text)
        return post_text

    @staticmethod
    def getAllArticlesTitlesAndLinks():
        # URL of the MEDIUM website
        url = "https://www.medium.com/"

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the article links on the page
        # article_links = soup.find_all("a", class_="Link__link___3dWao")
        article_links = soup.find_all("a")
        # Print the titles and URLs of the articles
        try:
            results_list = []
            for link in article_links:
                title = link.text.strip()
                if len(str(link)) > 0:
                    url = link["href"]
                    if title:
                        print(title)
                        print(url)
                        results_list.append("link title=" + title + "***" + "link url=" + str(url))
            print(results_list)
        except Exception as error:
            # handle the exception
            print("An exception occurred:", error)  # An exception occurred:

        return results_list
    @staticmethod
    def scrape_image_urls():
        url = "https://www.medium.com/"
        # Send a GET request to the post URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all image tags
        image_tags = soup.find_all("img")

        # Extract the URLs from the 'src' attribute of the image tags
        image_urls = []
        for tag in image_tags:
            image_url = tag.get("src")
            if image_url:
                print(image_url)
                image_urls.append(image_url)

        return image_urls

# URL of the Medium po


if __name__ == "__main__":
    # MediumScrraper.getPostsFullText()
    #MediumScrraper.getAllArticlesTitlesAndLinks()
    MediumScrraper.scrape_image_urls()
    # article_url1='https://edition.cnn.com/2023/05/18/asia/g7-summit-japan-key-issues-analysis-intl-hnk/index.html'
    # MediumScrraper.scrape_article_text(article_url1)
    # article_url2 = "https://edition.cnn.com/2023/05/17/americas/harry-meghan-car-crash-intl/index.html"
    # MediumScrraper.scrape_article_text(article_url2)
    # MediumScrraper.getArticalesHeaderText()
