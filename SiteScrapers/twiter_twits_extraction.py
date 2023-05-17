import requests
from bs4 import BeautifulSoup
from lxml import html
import requests
from playwright.sync_api import sync_playwright, playwright
import os


class TwitterExtraction:
    @staticmethod
    def playwright_on_chrome():
        playwright = sync_playwright().start()

        user_dir = '/tmp/playwright'
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        # browser = playwright.chromium.launch(channel='msedge', headless=False)
        #context = playwright.chromium.launch_persistent_context(user_data_dir=user_dir, headless=False)
        context = playwright.chromium.launch(headless=False)
        page = context.new_page()
        page.goto('https://twitter.com/home')
        page_source = page.inner_html("*")
        print("My url=" + page.url)
        tree = html.fromstring(page_source)
        # page.pause()
        # all_job_items_container = tree.xpath('//div')
        all_job_items_container = page.locator(f'[role="article"][data-testid="tweet"]')
        # if all_job_items_container.all_inner_texts() is not None:
        #     for i in range(4):
        #         print(all_job_items_container.all_inner_texts()[i])
        people_icon_pic = page.locator("xpath=//div[@class='css-1dbjc4n r-12181gd r-1pi2tsx r-1ny4l3l r-o7ynqc r-6416eg r-13qz1uu']")
        #elements = page.get_by_role("list").filter(has_text='More...').all()
        imgs = page.query_selector_all("img")
        for img in imgs:
            src = img.get_attribute("src")
            print(src)
        return {'result': page.title()}

    @staticmethod
    def mainCategories():
        url = 'https://www.ebay.com/n/all-categories'

    @staticmethod
    def get_ebay_search_phrases():
        url = "https://www.ebay.com/n/all-categories"

        payload = {}
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'aws-ubid-main=304-3562347-3461826; aws-account-alias=389387664392; remember-account=true; regStatus=registered; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A389387664392%3Auser%2Fniv-admin%22%2C%22alias%22%3A%22389387664392%22%2C%22username%22%3A%22niv-admin%22%2C%22keybase%22%3A%2251qBse7W7BQRQrrFX6EUYNVI%2Fj5bM%2FV3YbY%2BNKEZZr8%5Cu003d%22%2C%22issuer%22%3A%22https%3A%2F%2Fwww.amazon.com%2Fap%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJldS1ub3J0aC0xIiwiYWxnIjoiRVMzODQiLCJraWQiOiIwNDdjY2ZiZS1kOTkzLTQ3ODQtYTg5Mi0zZDQxNDQ5ZjgzNmEifQ.eyJzdWIiOiIzODkzODc2NjQzOTIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cHM6XC9cL3d3dy5hbWF6b24uY29tXC9hcFwvc2lnbmluIiwia2V5YmFzZSI6IjUxcUJzZTdXN0JRUlFyckZYNkVVWU5WSVwvajViTVwvVjNZYlkrTktFWlpyOD0iLCJhcm4iOiJhcm46YXdzOmlhbTo6Mzg5Mzg3NjY0MzkyOnVzZXJcL25pdi1hZG1pbiIsInVzZXJuYW1lIjoibml2LWFkbWluIn0.nTUyma0LikypEm2zmJrA6v-Rg7BSkXB5f7DIcuAEUhJoUZqfsTmxE2nEF71nUQNihGCAbA_t6T2_cV1Hk2SKMvJ9_V8SjM0c0PtWETUlWxHV4A5YKLRyP_mSQRF4R7v1; noflush_awsccs_sid=76483156fd458b30fcac5147c21a24d44e2cc42c838b02801c236135addea28c; aws-signer-token_eu-north-1=eyJrZXlWZXJzaW9uIjoiNU1Hcm9NYXFMb005V3A0MVJEeXRoMHRyNm5DSGpUV28iLCJ2YWx1ZSI6InFDWUM0eDBHZDNIQmFrNDNYOEw2YTJqSEtyaGMrNkJPQVVlWHI4QjhqTU09IiwidmVyc2lvbiI6MX0=; session-id=138-7565529-2438432; session-id-time=2082787201l; i18n-prefs=USD; skin=noskin; ubid-main=134-4001698-4902553; session-token=8+zxC5+xAfNMxDI33maablopyuu1j77RFgHT+x4R+WYrS2sDvHVBvIGGR+i3ESKP+LqhcVhcwOXYvjI2rcn/aOjMx7DubA+QMzx+VaYalVGOzsP8NSlaSEyoDLt5iiUfdnrjTdZEMZbow27bIiUQJP71mJA+Zq2Dwl3u7/u0r8DTMrpNeUly0VERmc4vmClWEmcUdmhD2lsfNDLePJCz4b3sj7ZL5VYoVZL12kxMQuQ=; session-token=x4vCaZeSwOSySB1oGnM/FWNCr5MeOK7Rb9Z1r4HEq5ZWWyb0A+yPfkxlgysNBelV8aADJTJN73IMPLchPg+xP7SQqt/NfBkXo9ANOXG9Zxd5y3MO/KFvCpJpXbnzWYkLChxXaf7f+3P3cHRrS+w1PUb557Bt2tzq6HApcbULA4yENx1RYKPnsQdnEeqNjhk1yVFylSwS628flnBUdKeYLNUVk6H4/QjTCmt2vSsZFys=',
            'Origin': 'https://www.amazon.com',
            'Referer': 'https://www.amazon.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # loop on json response
        res = []
        json = response.json()
        print(json)
        for item in json['suggestions']:
            res.append(item['value'])

        return res

    @staticmethod
    def get_twitter_default_twitts_details():
        # the eBay search URL
        query = 'home'

        url = 'https://twitter.com/' + query
        # make a GET request to the URL
        response = requests.get(url)


        # find all the search result items
        tree = html.fromstring(response.content)
        #items = tree.xpath("//div[@data-testid='cellInnerDiv' and starts-with(@style, 'transform: translate(')]")
        #items = tree.xpath("/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div")
        items=tree.xpath("//div")
        result_list = []
        # iterate over the items and extract the details
        for item in items:
            print(item.text_content())
            # extract the product title
            # restaurant_details = item.find('a', role='link')
            # print("product_details="+str(product_details));
            user_name =""

            # class ="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"
            if user_name:
                user_name_text = user_name.text.strip()
                # print('product_details_text='+product_details_text)
            else:
                user_name_text = 'N/A'

            price_category = item.find('p', class_='css-dzq7l1')
            # print("product_details="+str(product_details));
            if price_category:
                price_category_text = price_category.text.strip()
                # print('product_details_text='+product_details_text)
            else:
                price_category_text = 'N/A'

            restaurant_overview = item.find('p', class_="css-16lklrv")
            # print("product_details="+str(product_details));
            if restaurant_overview:
                restaurant_overview_text = restaurant_overview.text.strip()
                # print('product_details_text='+product_details_text)
            else:
                restaurant_overview_text = 'N/A'
            # extract the product price
            when_opened = item.find(class_='tagText__09f24__ArEfy iaTagText__09f24__Gv1CO css-chan6m')
            if when_opened:
                when_opened_text = when_opened.text.strip()
                # print("price="+price_text)
            else:
                when_opened_text = 'N/A'

            # extract the product URL
            url = item.find('a', itemprop='url')
            if url:
                url_text = url['href']
            else:
                url_text = 'N/A'

            #parent = soup.find_all(çlass_='css-9pa8cd')
            image = ""#parent.find('img', )
            if image:
                image_url = image['src']
            else:
                image_url = 'N/A'

            # print the product details
            print()
            print()
            # print(f'Title: {item_url}')
            print(f'IMAGE URL: {image_url}')
            print()
            result_item_details = '[[' + 'resturant_name:' + restaurant_details_text \
                                  + '  ' + 'link:' + url_text \
                                  + '  ' + 'image:' + image.text \
                                  + '  ' + 'price_category:' + price_category_text \
                                  + '  ' + 'when_opened:' + when_opened_text \
                                  + '  ' + 'restaurant_overview:' + restaurant_overview_text + ']]'
            result_list.append(result_item_details)
        print(len(result_list))
        return result_list


if __name__ == "__main__":
    TwitterExtraction.playwright_on_chrome()
