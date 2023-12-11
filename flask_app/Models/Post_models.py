# from scraper import twitter_scrape
from flask_app.Config.mysqlconnection import connectToMySQL

class Post():
    my_db = 'palestine_tweets'
    def __init__(self, data):
        self.id = data['id']
        self.official_id = data['official_id']
        self.post_avatar = data['tweet_avatar']
        self.url = data['url']
        self.query = data['query']
        self.post_id = data['tweet_id']
        self.text = data['text']
        self.username = data['username']
        self.fullname = data['fullname']
        self.timestamp = data['timestamp']
        self.replies = data['replies']
        self.retweets = data['retweets']
        self.likes = data['likes']
        self.quotes = data['quotes'],
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_post(cls, data, official_id):
        print("creating post")
        query = """
        INSERT INTO post (official_id,tweet_id ,tweet_avatar, url, query, text, username, fullname, timestamp, replies, likes, quotes)
        VALUES (%(official_id)s,%(tweet_id)s ,%(tweet_avatar)s, %(url)s, %(query)s, %(text)s, %(username)s, %(fullname)s, %(timestamp)s, %(replies)s, %(likes)s, %(quotes)s)
        """
        data = {
            'official_id': official_id,
            'tweet_id': data['tweet_id'],
            'tweet_avatar': data['tweet_avatar'],
            'url': data['url'],
            'query': data['query'],
            'text': data['text'],
            'username': data['username'],
            'fullname': data['fullname'],
            'timestamp': data['timestamp'],
            'replies': data['replies'],
            'likes': data['likes'],
            'quotes': data['quotes']

        }

        return connectToMySQL(cls.my_db).query_db(query, data)
    
    @classmethod
    def add_post_images(cls, data, post_id):
        query = """
        INSERT INTO images (post_id, image_url)
        VALUES (%(post_id)s, %(image_url)s)
        """

        data = {
            'post_id': post_id,
            'image_url': data['image_url']
        }

        return connectToMySQL(cls.my_db).query_db(query, data)
    
    @classmethod
    def get_posts(cls):
        query = """
        SELECT * FROM post
        """

        return connectToMySQL(cls.my_db).query_db(query)
    
    @classmethod
    def get_posts_by_id(cls, official_id):
        query = """
        SELECT *
        FROM post
        JOIN keywords ON INSTR(post.text, keywords.keyword) > 0
        WHERE post.official_id = %(official_id)s;
        """

        data = {
            'official_id': official_id
        }

        results = connectToMySQL(cls.my_db).query_db(query, data)
        posts = []
        repeated_posts = []
        for post in results:
            if post['tweet_id'] in repeated_posts:
                continue
            posts.append(cls(post))
            repeated_posts.append(post['tweet_id'])

        print(posts)
        if posts:
            return posts
        else:
            return False
    @classmethod
    def get_post_by_post_id(cls, post_id):
        query = """
        SELECT * FROM post WHERE (post_id = %(post_id)s) Limit 1
        """

        data = {
            'post_id': post_id
        }

        post =  cls(connectToMySQL(cls.my_db).query_db(query, data))

        return post
    
    @classmethod
    def update_post(cls, id, text):
        query = """
        UPDATE posts SET text = %(text)s WHERE id = %(id)s
        """

        data = {
            'text': text,
            'id': id
        }

        return connectToMySQL(cls.my_db).query_db(query, data)


    # @staticmethod
    # def create_rep_and_posts(officials_list):
    #     for official_data in officials_list:
    #         first_name, last_name, twitter_handle, state = official_data.split('\t')
        
    #         try:
    #             official_id = Official.create_official({
    #             'first_name': first_name,
    #             'last_name': last_name,
    #             'twitter_handle': twitter_handle,
    #             'state': state
    #             })
    #             print(f"Official created with ID: {official_id}")
    #         except Exception as e:
    #             print(f"Error creating official: {str(e)}")
    #             continue
        
    #         posts = twitter_scrape(twitter_handle, "2023-10-07")
    #         for post in posts:
    #             post_data = {
    #                 'post_avatar': post['post_avatar'],
    #                 'url': post['url'],
    #                 'query': post['query'],
    #                 'post_id': post['post_id'],
    #                 'text': post['text'],
    #                 'username': post['username'],
    #                 'fullname': post['fullname'],
    #                 'timestamp': post['timestamp'],
    #                 'replies': post['replies'],
    #                 'reposts': post['reposts'],
    #                 'likes': post['likes'],
    #                 'quotes': post['quotes']
    #             }

    #             try:
    #                 post_id = post.create_post(post_data, official_id)
    #                 print(f"post created with ID: {post_id}")
                
    #                 if len(post['images']) > 0:
    #                     for image in post['images']:
    #                         image_data = {'image_url': image}
    #                         post.add_post_images(image_data, post_id)
    #                         print(f"Image added to post")
    #             except Exception as e:
    #                 print(f"Error creating post: {str(e)}")
    
    #         return "posts created"

    # @staticmethod
    # def scrape_post(date):
    #     officials = Official.find_all_officials()
    #     for official in officials:
    #         posts = twitter_scrape(official.twitter_account, "2023-11-07")
    #         for post in posts:
    #             post_data = {
    #                 'post_avatar': post['post_avatar'],
    #                 'url': post['url'],
    #                 'query': post['query'],
    #                 'post_id': post['post_id'],
    #                 'text': post['text'],
    #                 'username': post['username'],
    #                 'fullname': post['fullname'],
    #                 'timestamp': post['timestamp'],
    #                 'replies': post['replies'],
    #                 'reposts': post['reposts'],
    #                 'likes': post['likes'],
    #                 'quotes': post['quotes']
    #             }

    #             try:
    #                 post_id = post.create_post(post_data, official.id)
    #                 print(f"post created with ID: {post_id}")
                    
    #                 if len(post['images']) > 0:
    #                     for image in post['images']:
    #                         image_data = {'image_url': image}
    #                         post.add_post_images(image_data, post_id)
    #                         print(f"Image added to post")
    #             except Exception as e:
    #                 print(f"Error creating post: {str(e)}")