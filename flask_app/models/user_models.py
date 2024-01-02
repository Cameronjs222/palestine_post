# official models ptyhon

from flask_app.config.mysqlconnection import connectToMySQL
from bcrypt import checkpw, gensalt, hashpw

class User():
    my_db = 'palestine_tweets'
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, form_data):
        query = """
        INSERT INTO users (username, password)
        VALUES (%(username)s, %(password)s)
        """

        if form_data['password'] != form_data['confirm_password']:
            return False
        
        data = {
            'username': form_data['username'],
            'password': hashpw(form_data['password'].encode(), gensalt()).decode()
        }
        return connectToMySQL(cls.my_db).query_db(query, data)
    
    @classmethod
    def get_user_by_username(cls, form_data):
        query = "SELECT * FROM users WHERE username = %(username)s;"

        data = {
            'username': form_data['username']
        }
        result = connectToMySQL(cls.my_db).query_db(query, data)
        if result == False:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate_login(data):
        user = User.get_user_by_username(data)
        if not user:
            return False
        if not checkpw(data['password'].encode(), user.password.encode()):
            return False
        return True