# official models ptyhon

from flask_app.config.mysqlconnection import connectToMySQL
from bcrypt import checkpw, gensalt, hashpw
import os
import json
from flask_app.models.Post_models import Post
from flask_app.models.Official_models import Official
import ijson


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
    @classmethod
    def read_and_save_to_database(cls, directory_path_variable):    
        json_data = []
        found_ids = set()  # Use a set to store non-repeating IDs
        not_found_ids = set()  # Use a set to store non-repeating not found IDs
        directory_path = os.path.join('C:\\Users\\camer\\projects\\palestine_post\\flask_app\\static\\', directory_path_variable)

        for filename in os.listdir(directory_path):
            if filename.endswith(".json"):
                with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                    parser = ijson.items(file, 'item')  # 'item' is the JSON root element
                    for post in parser:
                        official_id = Official.find_officials_by_username(post['username'][1:])
                        if official_id:
                            found_ids.add(official_id[0].id)
                            post_id = Post.create_post(post, official_id[0].id)
                            for img in post['images']:
                                img_data = {'image_url': img}
                                Post.add_post_images(img_data, post_id)
                        else:
                            not_found_ids.add(post['username'][1:])
                            continue
        sorted_found_ids = sorted(found_ids)
        print(sorted_found_ids)
        print(list(not_found_ids))


        # json_data = []
        # found_ids = []
        # not_found_ids = []
        # # flask_app\static\dataset_1 relative path
        # directory_path = os.path.join('C:\\Users\\camer\\projects\\palestine_post\\flask_app\\static\\', directory_path_variable)
        # print(directory_path)
        # for i, filename in enumerate(os.listdir(directory_path)):
        #     official_id = None
        #     if filename.endswith(".json"):
        #         with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
        #             if i > 14:
        #                 json_data = json.load(file)
        #                 official_id = Official.find_officials_by_username(json_data[0]['username'][1:])
        #                 if official_id:
        #                     found_ids.append(official_id[0].id)
        #                     for post in json_data:
        #                         post_id = Post.create_post(post, official_id[0].id)
        #                         for img in post['images']:
        #                             img_data = {'image_url': img}
        #                             Post.add_post_images(img_data, post_id)
        #                 else:
        #                     not_found_ids.append({'username': json_data[0]['username'][1:],'index': i,'filename': filename})
        #                     continue
        # sorted_found_ids = sorted(found_ids)
        # print(sorted_found_ids)
        # print(not_found_ids)

    @staticmethod
    def validate_login(data):
        user = User.get_user_by_username(data)
        if not user:
            return False
        if not checkpw(data['password'].encode(), user.password.encode()):
            return False
        return True