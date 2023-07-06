import sqlite3
from aifc import Error
import bcrypt


class DbOperations:
    user_id = 0

    def __init__(self, db_name):
        self.connection = None
        self.connect(db_name)
        self.db_name = db_name
        print("Opened database successfully")

    def connect(self, db_name):
        try:
            self.connection = sqlite3.connect('DbOperations/' + db_name)

        except Error as e:
            print(e)

    def get_user(self):
        query_result = ""
        sql_get_user_messages = 'select * from Users'

        data = self.connection.execute(sql_get_user_messages);
        print(data)
        for row in data:
            print("UserId = " + str(row[0]))
            query_result += str(row[0]) + " "
            print("Username = " + str(row[1]))
            query_result += str(row[1]) + " "
            print("Password = " + str(row[2]))
            query_result += str(row[2]) + "\n"

        self.connection.close()
        return query_result

    def check_user_exists(self, username):
        query_result = ""
        sql_get_user_count = 'select count(*) from Users where UserName=?'
        params = username

        cursor = self.connection.cursor()
        cursor.execute(sql_get_user_count, params)
        rows = cursor.fetchall()
        print(rows[0][0])

        self.connection.close();
        return query_result

    def get_user_id(self, username):
        sql_get_user_count = 'SELECT UserId FROM Users WHERE UserName = ?'

        cursor = self.connection.cursor()
        cursor.execute(sql_get_user_count, (username,))
        rows = cursor.fetchall()
        print(rows[0][0])
        query_result = rows[0][0]

        self.connection.close();
        return query_result

    def store_user_and_password_hash(self, username, password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

        insert_data_query = '''
            INSERT INTO Users (UserId,UserName, PasswordHash)
            VALUES (?, ?, ?);
        '''
        check_user_query = 'SELECT COUNT(*) FROM Users'
        cursor = self.connection.cursor()
        cursor.execute(check_user_query)
        result = cursor.fetchone()
        print(result)
        DbOperations.user_id = int(result[0]) + 1
        cursor.execute(insert_data_query, (DbOperations.user_id, username, password_hash))
        self.connection.commit()

    # Verify password
    def verify_password(self, username, password):
        select_data_query = '''
            SELECT PasswordHash FROM Users WHERE UserName = ?;
        '''
        cursor = self.connection.cursor()
        cursor.execute(select_data_query, (username,))
        result = cursor.fetchone()

        if result is not None:
            stored_hash = result[0]
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

        return False

    def insert_user_message(self, user_name, user_message,db_name):

        user_id = self.get_user_id(user_name)

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

    def get_all_messages(self, db_name):
        self.connect(db_name)
        all_messages_query = '''
                        select UserName,Message,Votes from Users,Messages where Users.UserId=Messages.UserId;
                    '''
        cursor = self.connection.cursor()
        data = cursor.execute(all_messages_query)

        query_result = ''

        for row in data:
            print("UserName = " + str(row[0]))
            query_result += " UserName = " + str(row[0]) + " "
            print("Message = " + str(row[1]))
            query_result += " Message = " + str(row[1])
            print("Votes = " + str(row[2]))
            query_result += " Votes = " + str(row[2]) + '\n'

        # Add line breaks
        query_result += '\n'

        print(query_result)
        self.connection.close();
        return query_result

    def user_vote_for_message(self, user_name, message_id, db_name, updated_votes):
        self.connect(db_name)
        cursor = self.connection.cursor()
        set_data_query = 'UPDATE Messages ' \
                         'set votes=' \
                         + str(updated_votes) \
                         + " where MessageId=" + str(message_id)

        cursor.execute(set_data_query)
        self.connection.commit()

    def get_current_message_votes(self, db_name, message_id):
        self.connect(db_name)
        get_current_votes_query = 'SELECT votes FROM Messages where MessageId=?'

        cursor = self.connection.cursor()
        cursor.execute(get_current_votes_query, (message_id,))
        result = cursor.fetchone()
        print(result)
        updated_votes = int(result[0])
        return updated_votes

    def is_user_message(self, db_name, message_id, user_name):
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

    def delete_message(self, message_id,db_name):
        self.connect(db_name)
        get_user_count = 'DELETE  FROM Messages where MessageId=?'

        cursor = self.connection.cursor()
        cursor.execute(get_user_count, (message_id,))
        self.connection.commit()
