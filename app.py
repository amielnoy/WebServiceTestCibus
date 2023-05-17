from SiteScrapers import amazon
from flask import Flask, jsonify, make_response

from SiteScrapers.IndeedScrraping.Indeed_positions_extraction import IndeedJobsExtraction
from SiteScrapers.ebay_products_extraction import EbayProductsExtraction
from SiteScrapers.yelp_products_extraction import YelpRestaurantsExtraction

app = Flask(__name__)


# @pytest.fixture(scope="function")
# def setup_browser_page(playwright: Playwright) -> Page:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     yield browser
#     browser.close()




@app.route('/amazon/searches')
def get_amazon_searches():
    return jsonify(amazon.get_amazon_search_phrases())


@app.route('/amazon/products')
def get_amazon_products():
    searches = amazon.get_amazon_search_phrases()
    return jsonify(amazon.get_amazon_data(searches[0]))


# EBAY
@app.route('/ebay/searches')
def get_ebay_searches():
    return jsonify(EbayProductsExtraction.get_ebay_search_phrases())


# EBAY
@app.route('/ebay/products')
def get_ebay_products():
    list_of_product_detail_items = EbayProductsExtraction.get_ebay_popular_product_details()
    return jsonify(list_of_product_detail_items)


# EBAY
# EBAY
@app.route('/yelp/Restaurants')
def get_yelp_default_resurant_details():
    restaurants_items_details_list = YelpRestaurantsExtraction.get_yelp_default_resurants_details()
    return jsonify(restaurants_items_details_list)


@app.route('/indeed/all_jobs')
def get_indeed():
    return IndeedJobsExtraction.get_jobs_playwright_on_chrome()


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
