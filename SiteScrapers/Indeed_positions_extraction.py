import requests
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright,playwright
import os

class IndeedJobsExtraction:
    @staticmethod
    def get_jobs_playwright_on_chrome():
        playwright = sync_playwright().start()

        user_dir = '/tmp/playwright'
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        #browser = playwright.chromium.launch(channel='msedge', headless=False)
        #context = playwright.chromium.launch_persistent_context(user_data_dir=user_dir, headless=False)
        context = playwright.chromium.launch( headless=False)
        page = context.new_page()
        url='https://www.indeed.com/l-midfield,-al-jobs.html?vjk=d5fa417e060f2640'
        page.goto(url)

        job_text_descriptions_list=[]
        print("My url=" + page.url)
        all_job_items_texts_list = page.locator('xpath=//div[@class="job_seen_beacon"]').all_inner_texts()
        for job_text in all_job_items_texts_list:
            job_text_descriptions_list.append(job_text)
        print(job_text_descriptions_list)

        all_job_links_list = page.locator('a')
        for job_link in all_job_links_list.all():
            print()
            print(job_link)

        job_link = page.locator("xpath=//div[@class='jobCard_mainContent big6_visualChanges']")
        #use java script and 'a' tag to locate all link jobs
        jobs_link_list = []
        all_links=page.eval_on_selector_all("a", "elements => elements.map(element => element.href)")
        for link in all_links:
            print("original link="+link)
            if not 'jobsearch' in str(link) and 'job' in str(link):
               jobs_link_list.append(link)
        #get links
        #list_count = all_job_items_texts_list.count()
        #page.pause()
        #elements = page.get_by_role("list").filter(has_text='More...').all()
        result_list = list(zip(jobs_link_list,job_text_descriptions_list))
        for result in result_list:
            print(result)
        return {'result': result_list}



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
    IndeedJobsExtraction.playwright_on_chrome()
