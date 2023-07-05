from DbOperations.DbOperations import DbOperations
from SiteScrapers import amazon
from flask import Flask, jsonify, make_response, request, redirect, url_for, render_template

from SiteScrapers.IndeedScrraping.Indeed_positions_extraction import IndeedJobsExtraction
from SiteScrapers.ebay_products_extraction import EbayProductsExtraction
from SiteScrapers.yelp_products_extraction import YelpRestaurantsExtraction

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


@app.route('/get_user/?user_name=')
def get_user():
    db_ops = DbOperations()
    db_ops.connect('UserMsgs.db')
    query_result = db_ops.get_user()
    return jsonify(query_result)


# GET requests will be blocked
@app.route('/register', methods=['POST'])
def register_user():
    request_data = request.get_json()

    username = request_data['UserName']
    password = request_data['Password']

    db_ops = DbOperations()
    db_ops.connect('UserMsgs.db')
    #db_ops.insert_new_user(username, password)
    db_ops.store_user_and_password_hash(username,password)

    is_password_verrified=db_ops.verify_password(username,password)
    if is_password_verrified:
        print("Password="+password+" VERIFIED!")
    else:
        print("Password=" + password + " NOT VVERIFIED!! ERROR!!")
    return jsonify("Wrote to Users table: user_name="+username+" Password="+password)

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        request_data = request.get_json()
        username = request_data['UserName']
        password = request_data['Password']
        db_ops = DbOperations()
        db_ops.connect('UserMsgs.db')

        if db_ops.verify_password(username,password):
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password.'
            #return render_template('login.html', error=error)
            return jsonify({'error': error}), 401
    return render_template('login.html')

# Home route (requires authentication)
@app.route('/home')
def home():
    # Example: Retrieve user-specific data based on session
    # user_id = session['user_id']
    # Retrieve user data from the database based on user_id
    # ...
    return 'Welcome to the home page!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
