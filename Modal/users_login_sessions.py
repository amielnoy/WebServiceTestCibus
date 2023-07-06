class UsersLoginSessions:
    user_logins = {}

    @staticmethod
    def add_user_login(username):
        # check user exists
        if username in UsersLoginSessions.user_logins.keys():
            if UsersLoginSessions.user_logins[username]:
                print("User=" + username + " already logged in!!")
        else:
            UsersLoginSessions.user_logins[username] = True

    @staticmethod
    def remove_user_login(username):
        # check user exists
        if username in UsersLoginSessions.user_logins.keys():
            if UsersLoginSessions.user_logins[username]:
                UsersLoginSessions.user_logins[username] = False
                print("User=" + username + "  logged out!!")
        else:
            print("User=" + username + " is not logged in!!")

    @staticmethod
    def is_user_logged_in(username):
        if username in UsersLoginSessions.user_logins.keys():
            if UsersLoginSessions.user_logins[username]:
                return True
        else:
            return False
