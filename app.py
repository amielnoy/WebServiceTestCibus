import json
import os
from http.client import HTTPException

from flask import Flask, jsonify, make_response, request, render_template
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from DbOperations.DbOperations import DbOperations
from Utils.exception_ops import print_exception_details
from Utils.users_login_sessions import UsersLoginSessions

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.urandom(12)
jwt = JWTManager(app)
db_name = 'UserMsgs.db'


# Register new user ,insert it's username & password to Users Table in the
# data base
@app.route('/register', methods=['POST'])
def register_user():
    try:
        request_data = request.get_json()

        username = request_data['UserName']
        password = request_data['Password']
    except Exception as exception_details:
        print_exception_details(exception_details)

    db_ops = DbOperations(db_name)
    # db_ops.insert_new_user(username, password)
    db_ops.store_user_and_password_hash(username, password)

    is_password_verrified = db_ops.verify_password(username, password)
    if is_password_verrified:
        print("Password=" + password + " VERIFIED!")
    else:
        print("Password=" + password + " NOT VVERIFIED!! ERROR!!")
    data={
        "UserMessage":"Wrote to Users table: user_name=" + username + " Password=" + password
    }
    return jsonify(data)


# Login to the system set the UserLoginSessions(saves all logged in users)
# Dictionary to set the current login user
@app.route('/login', methods=['POST'])
def login():
    global username, password

    try:
        request_data = request.get_json()
        username = request_data['UserName']
        password = request_data['Password']

    except Exception as exception_details:
        print_exception_details(exception_details)

    db_ops = DbOperations(db_name)

    if db_ops.verify_password(username, password):
        UsersLoginSessions.add_user_login(username)
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    else:
        error = 'Invalid username or password.'
        return jsonify({'error': error}), 401


# Logout the givven user(by username & password)
# Set him as **not logged in**
# in UserLoginSessions(saves all logged in users)
# Dictionary
@app.route('/logout', methods=['POST'])
def logout():
    global username, password
    if request.method == 'POST':
        try:
            request_data = request.get_json()
            username = request_data['UserName']
            password = request_data['Password']

        except Exception as exception_details:
            print_exception_details(exception_details)

        db_ops = DbOperations(db_name)

        if db_ops.verify_password(username, password):
            UsersLoginSessions.remove_user_login(username)
            data = {
                "user": username,
                "UserMessage": "logged OUT SUCCESFULY"
            }
            return jsonify(data)
        else:
            error = 'Invalid username or password.'
            # return render_template('login.html', error=error)
            return jsonify({'error': error}), 401
    return render_template('login.html')


# add message to the givven user messages
# only if he is already logged in
@app.route('/messages', methods=['POST'])
def add_message_to_user_messages():
    global username, message_text
    try:
        request_data = request.get_json()

        username = request_data['UserName']
        message_text = request_data['MessageText']
    except Exception as exception_details:
        print_exception_details(exception_details)

    db_ops = DbOperations(db_name)

    if UsersLoginSessions.is_user_logged_in(username):
        db_ops.insert_user_message(username, message_text, db_name)
        data={
              "Message":message_text,
              "Username": username,
              "UserMessage": " ADDED SUCCESFULY MESSAGE TO THE BOARD!"
              }
        return jsonify(data)
    else:
        return jsonify({"ERROR": "NOT ADDED,BECAUSE NOT LOGGED IN !"})


# Get all the messages stored at Messages table
# For all the users
@app.route('/messages', methods=['GET'])
def get_all_messages():
    db_ops = DbOperations(db_name)
    data = db_ops.get_all_messages(db_name)
    print(data)
    return jsonify(data)


# vote(up or down) for specific message by it's id
# and only if the user is looged in
# for voting up,
# parameter in the request body Vote='vote_up'
# for down, Vote='vote_down'
@app.route('/messages/<message_id>/vote', methods=['POST'])
def page(message_id):
    global username
    vote = ''
    try:
        request_data = request.get_json()
        username = request_data['UserName']
        vote = request_data['Vote']
    except Exception as exception_details:
        print_exception_details(exception_details)

    if UsersLoginSessions.is_user_logged_in(username):
        if vote == 'vote_up':
            vote = 1
        elif vote == 'vote_down':
            vote = -1

        db_ops = DbOperations(db_name)
        votes_before = db_ops.get_current_message_votes(db_name, message_id)
        updated_votes = votes_before + vote

        if updated_votes < 0:
            error_data = {
                "Messageid": message_id,
                "ERROR": "Cant Updated Votes below ZERO! Or message not EXISTS!"
            }
            return jsonify(error_data)
        else:
            db_ops.user_vote_for_message(username, message_id, db_name, updated_votes)
            data={
                "Messageid": message_id,
                "UpdatedVotes": updated_votes
            }
            return jsonify(data)
    else:
        data = {"User": username,
                "Message": "NOT LOGGED IN!"}
        return jsonify(data)


# Delete a specific message by it's id
# givving also the user name parameter,
# the user can only delete it's own messages
@app.route('/messages/<message_id>', methods=['DELETE'])
def delete_user_message(message_id):
    global username
    try:
        request_data = request.get_json()
        username = request_data['UserName']
    except Exception as exception_details:
        print_exception_details(exception_details)
    if UsersLoginSessions.is_user_logged_in(username):

        db_ops = DbOperations(db_name)
        is_user_message = db_ops.is_user_message(db_name, message_id, username)

        if is_user_message:
            db_ops.delete_message(message_id, db_name)
            data = {
                "MessageId": str(message_id),
                "UserMessage": "DELETED SUCCESFULY By User=" + username
            }
            return jsonify(data)
        else:
            error_data={
                "MessageId": str(message_id),
                "ERROR": "You can only delete your messages/or message not exists!"
            }
            return jsonify(error_data)
    else:
        data = {"User": username,
                "Message": "NOT LOGGED IN!"}
        return jsonify(data)


# Get all the user messages
# Only if the user is logged in
@app.route('/user/messages', methods=['GET'])
def get_all_user_messages():
    current_username = UsersLoginSessions.current_loged_in_username

    db_ops = DbOperations(db_name)

    if UsersLoginSessions.is_user_logged_in(current_username):
        data = db_ops.get_all_user_messages(db_name, current_username)
        print(data)
        return jsonify(data)
    else:
        report = " ERROR NO MESSAGES,BECAUSE USER NOT LOGGED IN ! "
        error_data={"error":report}
        print(error_data)
        return jsonify(error_data)


# Handale unautherised errors
# Sending you are Unauthorized! message to the user
# Because it lacks valid authentication credentials for the requested resource
@app.errorhandler(401)
def resource_not_found(e):
    return make_response(jsonify(error='you are Unauthorized!'), 401)


# Handale ERROR of Autherized user that don't have permission to this resource by sending
# you don't have permission to access this resource
# This is an HTTP status code that occurs when the web server understands the request
# but can't provide additional access
@app.errorhandler(403)
def resource_not_found(e):
    return make_response(jsonify(error='you don\'t have permission to access this resource!'), 403)


# 404 is a status code that tells a web user
# that a requested page is not available@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='full url Not found!'), 404)


# general error handler to give info
# on the current HTTP error
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
    app.run(host='0.0.0.0', port=5002)
