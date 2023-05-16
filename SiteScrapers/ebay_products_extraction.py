import requests
from bs4 import BeautifulSoup
import requests


class EbayProductsExtraction:
    @staticmethod
    def get_ebay_popular_product_details():
        # the eBay search URL
        url = 'https://www.ebay.com/globaldeals?_trkparms=' \
              + 'pageci%3A46b54439-f1c1-11ed-bad5-4201c6b7c2de%7Cparentrq%3A1681ec7b1880aaf4c952b4ecfffb7031%7Ciid%3A2'
        # make a GET request to the URL
        response = requests.get(url)

        # create a BeautifulSoup object
        soup = BeautifulSoup(response.content, 'html.parser')

        # find all the search result items
        items = soup.find_all('div', class_='dne-itemtile-detail')
        result_list = []
        res_item=""
        # iterate over the items and extract the details
        for item in items:
            # extract the product title
            product_details = item.find('a')
            # print("product_details="+str(product_details));
            if product_details:
                product_details_text = product_details.text.strip()
                # print('product_details_text='+product_details_text)
            else:
                title_text = 'N/A'

            # extract the product price
            price = item.find('span', class_='first')
            if price:
                price_text = price.text.strip()
                # print("price="+price_text)
            else:
                price_text = 'N/A'

            # extract the product URL
            url = item.find('a', itemprop='url')
            if url:
                url_text = url['href']
            else:
                url_text = 'N/A'

            parent = item.parent
            image = parent.find('img')
            if image:
                image_url = image['src']
            else:
                image_url = 'N/A'

            discount = item.find(class_="dne-itemtile-original-price")
            if discount:
                discount_text = discount.text.strip()
            else:
                discount_text = 'N/A'

            allmost_gone = item.find('span',
                                     class_='dne-itemcard-hotness itemcard-hotness-red dne-itemcard-hotness-with-badge')
            if allmost_gone:
                allmost_gone_text = allmost_gone.text.strip()
            else:
                allmost_gone_text = 'N/A'

            # print the product details
            print()
            print()
            print(f'Title: {product_details_text}')
            print(f'Price: {price_text}')
            print(f'IMAGE URL: {image_url}')
            print(f'DISCOUNT: {discount_text}')
            print(f'ALLMOST_GONE: {allmost_gone_text}')
            print()
            res_item = 'title :' + product_details_text \
                      + '\n'+'link:' + url_text \
                      + '\n' + 'image:' + image_url \
                      + "\n" + 'price:' + price_text \
                      + "\n" + 'discount:' + discount_text \
                      + "\n\n"
            result_list.append(res_item)
        print(len(result_list))
        return result_list

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


if __name__ == "__main__":
    EbayProductsExtraction.get_ebay_popular_product_details()
