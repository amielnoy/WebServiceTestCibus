import sqlite3
from aifc import Error

import bcrypt


class DbOperations:
    user_id = 0

    def __init__(self):
        self.connection = self.connection = None
        print("Opened database successfully");

    def connect(self, db_name):
        self.connection = None
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

        self.connection.close();
        return query_result

    # def insert_new_user(self, username, password):
    #     inser_data_query = ''' INSERT INTO Users(UserId,UserName,Password)
    #             VALUES(?,?,?) '''
    #     DbOperations.user_id += 1
    #     user_data = [(DbOperations.user_id, username, password)]
    #
    #     cursor = self.connection.cursor()
    #     print("after cursor creation")
    #     cursor.executemany(inser_data_query, user_data)
    #     print("after cursor.execute")
    #     self.connection.commit()
    #
    #     # Close the cursor and the connection
    #     cursor.close()
    #     self.connection.close()

    def store_user_and_password_hash(self,username, password):
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
        DbOperations.user_id=int(result[0])+1
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

    def insert_new_user_message(conn, user_message):
        """
      Create a new project into the projects table
      :param conn:
      :param project:
      :return: project id
      """
        sql = ''' INSERT INTO projects(name,begin_date,end_date)
                VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, user_message)
        conn.commit()
