import json
from http.client import HTTPException

from DbOperations.DbOperations import DbOperations
from SiteScrapers import amazon
from flask import Flask, jsonify, make_response, request, redirect, url_for, render_template

from SiteScrapers.IndeedScrraping.Indeed_positions_extraction import IndeedJobsExtraction
from SiteScrapers.ebay_products_extraction import EbayProductsExtraction
from SiteScrapers.yelp_products_extraction import YelpRestaurantsExtraction

app = Flask(__name__)

is_logged_in = False


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
    # db_ops.insert_new_user(username, password)
    db_ops.store_user_and_password_hash(username, password)

    is_password_verrified = db_ops.verify_password(username, password)
    if is_password_verrified:
        print("Password=" + password + " VERIFIED!")
    else:
        print("Password=" + password + " NOT VVERIFIED!! ERROR!!")
    return jsonify("Wrote to Users table: user_name=" + username + " Password=" + password)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


@app.errorhandler(401)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 401)


@app.errorhandler(403)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 403)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        request_data = request.get_json()
        username = request_data['UserName']
        password = request_data['Password']
        db_ops = DbOperations()
        db_ops.connect('UserMsgs.db')

        if db_ops.verify_password(username, password):
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password.'
            # return render_template('login.html', error=error)
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
