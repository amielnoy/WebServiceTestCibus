import urllib

import requests
from bs4 import BeautifulSoup


def get_amazon_data(search_phrase):
    url = "https://www.amazon.com/s?k=" \
          + urllib.parse.quote(search_phrase) \
          + "&i=aps&ref=nb_sb_ss_sx-trend-t-ps-d_2_0&crid=2B4HZDWJ8LOF0&sprefix=%2Caps%2C183"

    payload = {}
    headers = {
        'authority': 'www.amazon.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'aws-ubid-main=304-3562347-3461826; aws-account-alias=389387664392; remember-account=true; regStatus=registered; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A389387664392%3Auser%2Fniv-admin%22%2C%22alias%22%3A%22389387664392%22%2C%22username%22%3A%22niv-admin%22%2C%22keybase%22%3A%2251qBse7W7BQRQrrFX6EUYNVI%2Fj5bM%2FV3YbY%2BNKEZZr8%5Cu003d%22%2C%22issuer%22%3A%22https%3A%2F%2Fwww.amazon.com%2Fap%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJldS1ub3J0aC0xIiwiYWxnIjoiRVMzODQiLCJraWQiOiIwNDdjY2ZiZS1kOTkzLTQ3ODQtYTg5Mi0zZDQxNDQ5ZjgzNmEifQ.eyJzdWIiOiIzODkzODc2NjQzOTIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cHM6XC9cL3d3dy5hbWF6b24uY29tXC9hcFwvc2lnbmluIiwia2V5YmFzZSI6IjUxcUJzZTdXN0JRUlFyckZYNkVVWU5WSVwvajViTVwvVjNZYlkrTktFWlpyOD0iLCJhcm4iOiJhcm46YXdzOmlhbTo6Mzg5Mzg3NjY0MzkyOnVzZXJcL25pdi1hZG1pbiIsInVzZXJuYW1lIjoibml2LWFkbWluIn0.nTUyma0LikypEm2zmJrA6v-Rg7BSkXB5f7DIcuAEUhJoUZqfsTmxE2nEF71nUQNihGCAbA_t6T2_cV1Hk2SKMvJ9_V8SjM0c0PtWETUlWxHV4A5YKLRyP_mSQRF4R7v1; noflush_awsccs_sid=76483156fd458b30fcac5147c21a24d44e2cc42c838b02801c236135addea28c; aws-signer-token_eu-north-1=eyJrZXlWZXJzaW9uIjoiNU1Hcm9NYXFMb005V3A0MVJEeXRoMHRyNm5DSGpUV28iLCJ2YWx1ZSI6InFDWUM0eDBHZDNIQmFrNDNYOEw2YTJqSEtyaGMrNkJPQVVlWHI4QjhqTU09IiwidmVyc2lvbiI6MX0=; session-id=138-7565529-2438432; session-id-time=2082787201l; i18n-prefs=USD; skin=noskin; ubid-main=134-4001698-4902553; session-token=IgLkO3TF41sTSQ4AuQAQqACaLdBzD9nRQNPNxUnWwjPFJWERBOkHIJDodqAQEo8hVn+SmCF/OOpgvVJVzEXSnGwl1ZSrZwHGHIvVZ075hDV3Rs/a8RFCjnSJldzkZKl7NY3Tp5XzYBYdS+DhDDP5tdF2H7tDc6SJ4SFqnDtLBeBHSQ/bckRhgyJD/X3IbQX/UCiL0nrtPm050uT9ieXXN7LRoDPPts33bguIM4UGe20=; csm-hit=tb:41G8HY9C5XK5HM501NY1+b-JYG07EZ6CAW19VPS4JAT|1684000452790&t:1684000452790&adb:adblk_no; session-token=x4vCaZeSwOSySB1oGnM/FWNCr5MeOK7Rb9Z1r4HEq5ZWWyb0A+yPfkxlgysNBelV8aADJTJN73IMPLchPg+xP7SQqt/NfBkXo9ANOXG9Zxd5y3MO/KFvCpJpXbnzWYkLChxXaf7f+3P3cHRrS+w1PUb557Bt2tzq6HApcbULA4yENx1RYKPnsQdnEeqNjhk1yVFylSwS628flnBUdKeYLNUVk6H4/QjTCmt2vSsZFys=',
        'device-memory': '8',
        'downlink': '10',
        'dpr': '2',
        'ect': '4g',
        'referer': 'https://www.amazon.com/',
        'rtt': '0',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '2',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"12.5.0"',
        'sec-ch-viewport-width': '1170',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'service-worker-navigation-preload': 'true',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'viewport-width': '1170'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find specific elements using BeautifulSoup functions
    results = soup.findAll('h2', {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-3'})

    res = []
    for result in results:
        # Extract information from each element
        title = result.text
        parent = result.parent.parent.parent
        link_item = parent.find('a')
        link = ''
        if link_item:
            link = link_item['href']
        img = parent.find('img')
        image = ''
        if img:
            image = img['src']
        price_item = parent.find('span', {'class': 'a-offscreen'})
        price = ''
        if price_item:
            price = price_item.text
        stars = ''
        star_item = parent.find('i', {'class': 'a-icon-star-small'})
        if star_item:
            # get all classes
            stat_text = star_item.find('span', {'class': 'a-icon-alt'})
            if stat_text:
                stars = stat_text.text.split(' ')[0]
        prime = ''
        prime_item = parent.find('div', {'class': 'a-row a-size-base a-color-secondary s-align-children-center'})
        if prime_item:
            prime_text = prime_item.findAll('span', {'class': 'a-color-base'})
            # map prime_text to list of strings
            p_text_list = list(map(lambda x: x.text, prime_text))
            prime = ",".join(p_text_list)

        raters = ''
        raters_item = parent.find('span', {'class': 'a-size-base s-underline-text'})
        if raters_item:
            raters = raters_item.text
        print(f'Title: {title}, Link: {link}, Image: {image}, Price: {price}')
        # Add new item to the list
        res.append({
            'title': title,
            'link': link,
            'image': image,
            'price': price,
            'stars': stars,
            'prime': prime,
            'raters': raters
        })
    return res


def get_amazon_search_phrases():
    import requests

    url = "https://completion.amazon.com/api/2017/suggestions?limit=11&prefix=&suggestion-type=WIDGET&suggestion-type=KEYWORD&page-type=Gateway&alias=aps&site-variant=desktop&version=3&event=onfocus&wc=&lop=en_US&last-prefix=%00&avg-ks-time=4632&fb=1&session-id=138-7565529-2438432&request-id=JYG07EZ6CAW19VPS4JAT&mid=ATVPDKIKX0DER&plain-mid=1&client-info=amazon-search-ui"

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
