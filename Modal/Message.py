class Message:
    def __init__(self, user_id, message):
        self.message=message
        self.user_id=user_id
    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message=message

    def get_user_id(self):
        return self.get_user_id()

    def set_user_id(self, user_id):
        self.user_id= user_id
