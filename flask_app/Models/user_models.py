# official models ptyhon

from flask_app.config.mysqlconnection import connectToMySQL
from bcrypt import checkpw, gensalt, hashpw

class User():
    my_db = 'palistine_posts'
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = """
        INSERT INTO user (username, password)
        VALUES (%(username)s, %(password)s)
        """
        return connectToMySQL(cls.my_db).query_db(query, data)
    
    @classmethod
    def get_user_by_username(cls, data):
        query = "SELECT * FROM user WHERE username = %(username)s;"
        result = connectToMySQL(cls.my_db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate_login(data):
        user = User.get_user_by_username(data)
        if not user:
            return False
        return True