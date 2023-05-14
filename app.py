from SiteScrapers import amazon
from flask import Flask, jsonify, make_response

app = Flask(__name__)


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
    return jsonify(amazon.get_amazon_search_phrases())
# EBAY
@app.route('/ebay/products')
def get_ebay_products():
    searches = amazon.get_amazon_search_phrases()
    return jsonify(amazon.get_amazon_data(searches[0]))


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)