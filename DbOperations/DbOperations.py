import sqlite3
from aifc import Error
from pathlib import Path

import bcrypt
from flask import jsonify

from Utils.exception_ops import print_exception_details


class DbOperations:
    user_id = 0

    # Get the full path of the project root as Path object
    def get_project_root(self) -> Path:
        return Path(__file__).parent.parent

    # Constructor to initialize
    # Connection and set it to the local Database
    # And set the db name
    def __init__(self, db_name):
        self.connection = None
        self.connect(db_name)
        print("Opened database successfully")

    # Create db connection to the local sqlite3 db
    def connect(self, db_name):
        try:
            self.connection = sqlite3.connect(str(self.get_project_root()) + '/DbOperations/' + db_name)
        except Exception as exception_details:
            print_exception_details(exception_details)

    # get user 0 or 1 apearnces in Users table
    def check_user_exists(self, username):
        query_result = ""
        sql_get_user_count = 'select count(*) from Users where UserName=?'
        params = username
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_get_user_count, params)
            rows = cursor.fetchall()
            print(rows[0][0])

            self.connection.close()
            return query_result
        except Exception as exception_details:
            print_exception_details(exception_details)

    # Get user id from Users table
    # If user exists!
    def get_user_id(self, username):
        sql_get_user_count = 'SELECT UserId FROM Users WHERE UserName = ?'
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_get_user_count, (username,))
            rows = cursor.fetchall()
            print(rows[0][0])
            query_result = rows[0][0]

            self.connection.close();
            return query_result
        except Exception as exception_details:
            print_exception_details(exception_details)

    # Write the username to the Users table
    # Write Encrypted version of the pasdword to Users DB table
    def store_user_and_password_hash(self, username, password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

        insert_data_query = '''
            INSERT INTO Users (UserId,UserName, PasswordHash)
            VALUES (?, ?, ?);
        '''
        check_user_query = 'SELECT COUNT(*) FROM Users'
        try:
            cursor = self.connection.cursor()
            cursor.execute(check_user_query)
            result = cursor.fetchone()
            print(result)
            DbOperations.user_id = int(result[0]) + 1
            cursor.execute(insert_data_query, (DbOperations.user_id, username, password_hash))
            self.connection.commit()
        except Exception as exception_details:
            print_exception_details(exception_details)

    # Verify password correctness
    # Using the input password to create Encrypted password
    # and comparing it to Encripted password in the Users Db Table Users
    def verify_password(self, username, password):
        select_data_query = '''
            SELECT PasswordHash FROM Users WHERE UserName = ?;
        '''
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_data_query, (username,))
            result = cursor.fetchone()

            if result is not None:
                stored_hash = result[0]
                return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

            return False
        except Exception as exception_details:
            print_exception_details(exception_details)

    # Insert Message to the specific user by user Id
    # in the Messages DB table
    def insert_user_message(self, user_name, user_message, db_name):

        user_id = self.get_user_id(user_name)
        try:
            self.connect(db_name)
            check_user_query = 'SELECT MAX(MessageId) FROM Messages'

            cursor = self.connection.cursor()
            cursor.execute(check_user_query)
            result = cursor.fetchone()
            print(result)
            message_id = int(result[0]) + 1

            insert_data_query = '''
                            INSERT INTO Messages (MessageId,UserId,Message,Votes)
                            VALUES (?, ?, ?,?);
                        '''
            votes = 0
            cursor.execute(insert_data_query, (message_id, user_id, user_message, votes))
            self.connection.commit()
        except Exception as exception_details:
            print_exception_details(exception_details)

    # Get all the messages(for all users)
    # Stored at Messages table
    def get_all_messages(self, db_name):
        self.connect(db_name)
        all_messages_query = '''
                        select UserName,Message,Votes from Users,Messages where Users.UserId=Messages.UserId;
                    '''
        try:
            cursor = self.connection.cursor()
            data = cursor.execute(all_messages_query)

            combined_json = {}
            i = 0
            for row in data:
                json_object = {
                    "UserName": str(row[0]),
                    "Message": str(row[1]),
                    "Votes": str(row[2])
                }
                combined_json[f"message{i + 1}"] = json_object
                i += 1


            print(combined_json)
            self.connection.close()
            return combined_json
        except Exception as exception_details:
            print_exception_details(exception_details)

    # Get all the messages for a givven user
    # From Messages DB Table
    def get_all_user_messages(self, db_name, user_name):
        try:
            self.connect(db_name)
            user_id = self.get_user_id(user_name)
            self.connect(db_name)
            all_user_messages_query = "select Message,votes from Messages" \
                                      " where Userid=" \
                                      + str(user_id)

            cursor = self.connection.cursor()
            data = cursor.execute(all_user_messages_query)

            combined_json = {}
            i = 0
            for row in data:
                json_object = {
                    "Message": str(row[0]),
                    "Votes": str(row[1])
                }
                combined_json[f"message{i + 1}"] = json_object
                i += 1

            print(combined_json)
            self.connection.close()
            return combined_json
        except Exception as exception_details:
            print_exception_details(exception_details)

    # Increase /Decrease by one the votes field
    # for specific user message in Messages table
    def user_vote_for_message(self, user_name, message_id, db_name, updated_votes):
        try:
            self.connect(db_name)
            cursor = self.connection.cursor()
            set_data_query = 'UPDATE Messages ' \
                             'set votes=' \
                             + str(updated_votes) \
                             + " where MessageId=" + str(message_id)

            cursor.execute(set_data_query)
            self.connection.commit()
        except Exception as exception_details:
            print_exception_details(exception_details)

    def get_current_message_votes(self, db_name, message_id):
        try:
            self.connect(db_name)
            get_current_votes_query = 'SELECT votes FROM Messages where MessageId=?'

            cursor = self.connection.cursor()
            cursor.execute(get_current_votes_query, (message_id,))
            result = cursor.fetchone()
            print(result)
            updated_votes = int(result[0])
            return updated_votes
        except Exception as exception_details:
            print_exception_details(exception_details)
            return -100

    # Verify if givven message belongs to specific user
    # By it's MessageId and UserId
    # Return True/false accordingly
    def is_user_message(self, db_name, message_id, user_name):
        try:
            self.connect(db_name)
            user_id = self.get_user_id(user_name)
            self.connect(db_name)
            get_user_count = 'SELECT count(*) FROM Messages where MessageId=? and UserId=?'

            cursor = self.connection.cursor()
            cursor.execute(get_user_count, (message_id, user_id))
            result = cursor.fetchone()
            print(result)
            user_count = int(result[0])
            return user_count == 1
        except Exception as exception_details:
            print_exception_details(exception_details)
            return False

    # Delete a message by it's MessageId from messages table
    def delete_message(self, message_id, db_name):
        try:
            self.connect(db_name)
            get_user_count = 'DELETE  FROM Messages where MessageId=?'

            cursor = self.connection.cursor()
            cursor.execute(get_user_count, (message_id,))
            self.connection.commit()
        except Exception as exception_details:
            print_exception_details(exception_details)
