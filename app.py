import json
from http.client import HTTPException

from DbOperations.DbOperations import DbOperations
from flask import Flask, jsonify, make_response, request, redirect, url_for, render_template

from Modal.users_login_sessions import UsersLoginSessions

app = Flask(__name__)
db_name = 'UserMsgs.db'


@app.route('/get_user/?user_name=')
def get_user():
    db_ops = DbOperations(db_name)
    query_result = db_ops.get_user()
    return jsonify(query_result)


# GET requests will be blocked
@app.route('/register', methods=['POST'])
def register_user():
    request_data = request.get_json()

    username = request_data['UserName']
    password = request_data['Password']

    db_ops = DbOperations(db_name)
    # db_ops.insert_new_user(username, password)
    db_ops.store_user_and_password_hash(username, password)

    is_password_verrified = db_ops.verify_password(username, password)
    if is_password_verrified:
        print("Password=" + password + " VERIFIED!")
    else:
        print("Password=" + password + " NOT VVERIFIED!! ERROR!!")
    return jsonify("Wrote to Users table: user_name=" + username + " Password=" + password)


# Login route
@app.route('/login', methods=['POST'])
def login():
    username = ''
    if request.method == 'POST':

        try:
            request_data = request.get_json()
            username = request_data['UserName']
            password = request_data['Password']

        except Exception as exception_details:
            print(type(exception_details))  # the exception type
            print(exception_details.args)  # arguments stored in .args
            print(exception_details)
            return jsonify(
                str(type(exception_details)) + " " + str(exception_details.args) + " " + str(exception_details))

        db_ops = DbOperations(db_name)

        if db_ops.verify_password(username, password):
            UsersLoginSessions.add_user_login(username)
            return jsonify('user=' + username + ' logged in SUCCESFULY')
        else:
            error = 'Invalid username or password.'
            # return render_template('login.html', error=error)
            return jsonify({'error': error}), 401


@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        try:
            request_data = request.get_json()
            username = request_data['UserName']
            password = request_data['Password']

        except Exception as exception_details:
            print(type(exception_details))  # the exception type
            print(exception_details.args)  # arguments stored in .args
            print(exception_details)
            return jsonify(
                str(type(exception_details)) + " " + str(exception_details.args) + " " + str(exception_details))

        db_ops = DbOperations(db_name)

        if db_ops.verify_password(username, password):
            UsersLoginSessions.remove_user_login(username)
            return jsonify("user=" + username + " logged out succesfuly!")
        else:
            error = 'Invalid username or password.'
            # return render_template('login.html', error=error)
            return jsonify({'error': error}), 401
    return render_template('login.html')


@app.route('/messages', methods=['POST'])
def add_message_to_user_messages():
    try:
        request_data = request.get_json()

        username = request_data['UserName']
        message_text = request_data['MessageText']
    except Exception as exception_details:
        print(type(exception_details))  # the exception type
        print(exception_details.args)  # arguments stored in .args
        print(exception_details)
        return jsonify(str(type(exception_details)) + " " + str(exception_details.args) + " " + str(exception_details))

    db_ops = DbOperations(db_name)

    report = "Message=" + message_text + "  for user=" + username
    if UsersLoginSessions.is_user_logged_in(username):
        db_ops.insert_user_message(username, message_text, db_name)
        report = report + " ADDED SUCCESFULY MESSAGE TO THE BOARD!"
        print(report)
    else:
        report = report + " ERROR NOT ADDED,BECAUSE NOT LOGGED IN ! "
        print(report)

    return jsonify(report)


@app.route('/messages', methods=['GET'])
def get_all_messages():
    db_ops = DbOperations(db_name)
    data = db_ops.get_all_messages(db_name)
    print(data)
    return jsonify(data)


# Home route (requires authentication)
@app.route('/messages/<message_id>/vote', methods=['POST'])
def page(message_id):
    try:
        request_data = request.get_json()
        username = request_data['UserName']
        vote = request_data['Vote']
    except Exception as exception_details:
        print(type(exception_details))  # the exception type
        print(exception_details.args)  # arguments stored in .args
        print(exception_details)
        return jsonify(str(type(exception_details)) + " " + str(exception_details.args) + " " + str(exception_details))
    if UsersLoginSessions.is_user_logged_in(username):
        if vote == 'vote_up':
            vote = 1
        elif vote == 'vote_down':
            vote = -1

        db_ops = DbOperations(db_name)
        votes_before = db_ops.get_current_message_votes(db_name, message_id)
        updated_votes=votes_before + vote

        if updated_votes < 0:
            return jsonify("MessageId=" + str(message_id) + "Cant Updated Votes below ZERO!")
        else:
            db_ops.user_vote_for_message(username, message_id, db_name, updated_votes)
            return jsonify("MessageId=" + str(message_id) + " Updated Votes=" + str(updated_votes))
    else:
        return jsonify("User="+username+"NOT LOGGED IN!")


@app.route('/messages/<message_id>', methods=['DELETE'])
def delete_user_message(message_id):
    try:
        request_data = request.get_json()
        username = request_data['UserName']
    except Exception as exception_details:
        print(type(exception_details))  # the exception type
        print(exception_details.args)  # arguments stored in .args
        print(exception_details)
        return jsonify(str(type(exception_details)) + " " + str(exception_details.args) + " " + str(exception_details))
    if UsersLoginSessions.is_user_logged_in(username):

        db_ops = DbOperations(db_name)
        is_user_message = db_ops.is_user_message(db_name,message_id,username)

        if is_user_message:
            db_ops.delete_message(message_id,db_name)
            return jsonify("MessageId=" + str(message_id) + " DELETED SUCCESFULY By User=" + username)
        else:
            return jsonify("MessageId=" + str(message_id) + "You can only delete your messages")
    else:
        return jsonify("User="+username+"NOT LOGGED IN!")


@app.route('/home')
def home():
    # Example: Retrieve user-specific data based on session
    # user_id = session['user_id']
    # Retrieve user data from the database based on user_id
    # ...
    return 'Welcome to the home page!'


@app.errorhandler(401)
def resource_not_found(e):
    return make_response(jsonify(error='you are Unauthorized!'), 401)


@app.errorhandler(403)
def resource_not_found(e):
    return make_response(jsonify(error='you don\'t have permission to access this resource!'), 403)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
