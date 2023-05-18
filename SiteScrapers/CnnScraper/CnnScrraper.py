import requests
from bs4 import BeautifulSoup


class CnnScrraper:

    @staticmethod
    def getArticalesHeaderText():
        url = "https://www.cnn.com/"

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the article headline elements
        #headline_elements = soup.find_all("a", class_="container__link container_lead-package__link container_lead-package__left container_lead-package__light")
        headline_elements = soup.find_all("span", {'data-editable':'headline'})
        # Extract and print the text of the article headlines
        headline_list=[]
        for headline in headline_elements:
            headline_text = headline.get_text()
            headline_list.append(headline_text)
            print(headline_text)
        return headline_list
    @staticmethod
    def getAllArticlesLinks():
        # URL of the CNN website
        url = "https://www.cnn.com/"

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
    def scrape_article_text(url):
        # Send a GET request to the article URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the article text elements
        article_text_elements = soup.find_all("p", class_="paragraph inline-placeholder")

        # Extract and concatenate the text from the article text elements
        article_text = ""
        for element in article_text_elements:
            article_text += element.text.strip() + " "
        print(article_text)
        return article_text

        # URL of the article to scrape

if __name__ == "__main__":
    #CnnScrraper.getAllArticlesLinks()
    article_url1='https://edition.cnn.com/2023/05/18/asia/g7-summit-japan-key-issues-analysis-intl-hnk/index.html'
    CnnScrraper.scrape_article_text(article_url1)
    article_url2 = "https://edition.cnn.com/2023/05/17/americas/harry-meghan-car-crash-intl/index.html"
    CnnScrraper.scrape_article_text(article_url2)
    #CnnScrraper.getArticalesHeaderText()