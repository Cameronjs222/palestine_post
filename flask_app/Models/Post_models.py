# from scraper import twitter_scrape
from flask_app.Config.mysqlconnection import connectToMySQL
# from official_model import Official

class Post():
    my_db = 'palestine_post'
    def __init__(self, data):
        self.id = data['id']
        self.official_id = data['official_id']
        self.tweet_avatar = data['tweet_avatar']
        self.url = data['url']
        self.query = data['query']
        self.tweet_id = data['tweet_id']
        self.text = data['text']
        self.username = data['username']
        self.fullname = data['fullname']
        self.timestamp = data['timestamp']
        self.replies = data['replies']
        self.retweets = data['retweets']
        self.likes = data['likes']
        self.quotes = data['quotes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_tweet(cls, data, official_id):
        query = """
        INSERT INTO post (official_id, tweet_avatar, url, query, tweet_id, text, username, fullname, timestamp, replies, retweets, likes, quotes)
        VALUES (%(official_id)s, %(tweet_avatar)s, %(url)s, %(query)s, %(tweet_id)s, %(text)s, %(username)s, %(fullname)s, %(timestamp)s, %(replies)s, %(retweets)s, %(likes)s, %(quotes)s)
        """
        data = {
            'official_id': official_id,
            'tweet_avatar': data['tweet_avatar'],
            'url': data['tweet_url'],
            'query': data['query'],
            'tweet_id': data['tweet_id'],
            'text': data['text'],
            'username': data['username'],
            'fullname': data['fullname'],
            'timestamp': data['timestamp'],
            'replies': data['replies'],
            'retweets': data['retweets'],
            'likes': data['likes'],
            'quotes': data['quotes']

        }

        return connectToMySQL(cls.my_db).query_db(query, data)
    
    @classmethod
    def add_tweet_images(cls, data, tweet_id):
        query = """
        INSERT INTO images (post_id, image_url)
        VALUES (%(post_id)s, %(image_url)s)
        """

        data = {
            'post_id': tweet_id,
            'image_url': data['image_url']
        }

        return connectToMySQL(cls.my_db).query_db(query, data)
    
    @classmethod
    def get_tweets(cls):
        query = """
        SELECT * FROM post
        """

        return connectToMySQL(cls.my_db).query_db(query)
    
    @classmethod
    def get_tweets_by_id(cls, official_id):
        # write a query to get all tweets by official id and check to see if post twitter_handle is in post column title query
        query = """
        SELECT p.* 
        From post p
        Where official_id=2
        And p.query like ''  

        """

        data = {
            'official_id': official_id
        }
        # check if tweet contains anthing
        tweet =  connectToMySQL(cls.my_db).query_db(query, data)
        if tweet:
            return tweet
        else:
            return [{'text': 'No tweets found'}]
    
    @classmethod
    def get_tweet_by_tweet_id(cls, tweet_id):
        query = """
        SELECT * FROM post WHERE (tweet_id = %(tweet_id)s) Limit 1
        """

        data = {
            'tweet_id': tweet_id
        }

        tweet =  cls(connectToMySQL(cls.my_db).query_db(query, data))

        return tweet
    
    @classmethod
    def update_tweet(cls, id, text):
        query = """
        UPDATE tweets SET text = %(text)s WHERE id = %(id)s
        """

        data = {
            'text': text,
            'id': id
        }

        return connectToMySQL(cls.my_db).query_db(query, data)



def create_rep_and_tweets(officials_list):
    for official_data in officials_list:
        first_name, last_name, twitter_handle, state = official_data.split('\t')
        
        try:
            official_id = Official.create_official({
                'first_name': first_name,
                'last_name': last_name,
                'twitter_handle': twitter_handle,
                'state': state
            })
            print(f"Official created with ID: {official_id}")
        except Exception as e:
            print(f"Error creating official: {str(e)}")
            continue
        
        tweets = twitter_scrape(twitter_handle, "2023-10-07")
        for tweet in tweets:
            tweet_data = {
                'tweet_avatar': tweet['tweet_avatar'],
                'url': tweet['url'],
                'query': tweet['query'],
                'tweet_id': tweet['tweet_id'],
                'text': tweet['text'],
                'username': tweet['username'],
                'fullname': tweet['fullname'],
                'timestamp': tweet['timestamp'],
                'replies': tweet['replies'],
                'retweets': tweet['retweets'],
                'likes': tweet['likes'],
                'quotes': tweet['quotes']
            }

            try:
                post_id = Tweet.create_tweet(tweet_data, official_id)
                print(f"Tweet created with ID: {post_id}")
                
                if len(tweet['images']) > 0:
                    for image in tweet['images']:
                        image_data = {'image_url': image}
                        Tweet.add_tweet_images(image_data, post_id)
                        print(f"Image added to tweet")
            except Exception as e:
                print(f"Error creating tweet: {str(e)}")
    
    return "Tweets created"

