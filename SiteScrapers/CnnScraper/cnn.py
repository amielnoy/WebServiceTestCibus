import requests
from bs4 import BeautifulSoup
from sqlalchemy import text

from config import Session


class CnnScraper:

    @staticmethod
    def getAllArticlesTitlesAndLinks():
        url = 'https://edition.cnn.com/'
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the post text elements
        zones = soup.find_all("div", class_="zone zone--t-light")

        print("Number of zones found: ", len(zones))
        res = []
        for zone in zones:
            category = ''
            #find h2 with class container__title-text container_lead-plus-headlines__title-text
            h2 = zone.find('h2', class_='container__title-text container_lead-plus-headlines__title-text')
            if h2:
                category = h2.text.strip()
            h2 = zone.find('h2', class_='container__title-text container_lead-plus-headlines-with-images__title-text')
            if h2:
                category = h2.text.strip()

            #get all links
            links = zone.find_all('a')
            for link in links:
                link.find('span')
                title = link.text.strip()
                link = link.get('href')
                if ('Show' in title and 'all' in title ):
                    category = link
                else:
                    if (not category == ''):
                        title = title.replace('\n', '')
                        res.append({'category':  category, 'title': title, 'link': link})
                        print(f'category: {category}, Title: {title}, Link: {link}')
        #print(res)
        query1 = text("insert into cnn(created_at,  category, title, link) values ( \
            now(), :category, :title, :link )")
        Session.execute(query1,res)
        print("after insert")
        Session.commit()
        return res

# URL of the Medium po


if __name__ == "__main__":
    # MediumScrraper.getPostsFullText()
    #MediumScrraper.getAllArticlesTitlesAndLinks()
    CnnScraper.getAllArticlesTitlesAndLinks()
    # article_url1='https://edition.cnn.com/2023/05/18/asia/g7-summit-japan-key-issues-analysis-intl-hnk/index.html'
    # MediumScrraper.scrape_article_text(article_url1)
    # article_url2 = "https://edition.cnn.com/2023/05/17/americas/harry-meghan-car-crash-intl/index.html"
    # MediumScrraper.scrape_article_text(article_url2)
    # MediumScrraper.getArticalesHeaderText()