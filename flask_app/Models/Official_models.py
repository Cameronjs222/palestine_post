from flask_app.Config.mysqlconnection import connectToMySQL
# Create your models here.

class Official():
    my_db = 'palestine_post'
    def __init__(self, id, first_name, last_name, twitter_handle, state, district):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.twitter_handle = twitter_handle
        self.state = state
        self.district = district

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'twitter_handle': self.twitter_handle,
            'state': self.state,
            'district': self.district
        }
    
    # Find offical by first and last name
    @classmethod
    def find_official_by_name(cls, first_name, last_name):
        query = """
        SELECT * FROM officials WHERE first_name = %(first_name)s AND last_name = %(last_name)s
        """

        data = {
            'first_name': first_name,
            'last_name': last_name
        }

        return connectToMySQL(cls.my_db).query_db(query, data)
    
    @classmethod
    def find_all_officials(cls):
        query = """
        SELECT * FROM officials
        """
        results = connectToMySQL(cls.my_db).query_db(query)
        list_of_officials = []
        for result in results:
            official = Official(result['id'], result['first_name'], result['last_name'], result['twitter_handle'], result['state'], result['district'])
            list_of_officials.append(official)

        return list_of_officials
    @classmethod
    def create_official(cls, user_data):
        print(user_data)
        query = """
        INSERT INTO officials (first_name, last_name, twitter_handle, state ) 
        VALUES (%(first_name)s, %(last_name)s, %(twitter_handle)s, %(state)s)
        """
        # add party, state, district and , %(party)s, %(state)s, %(district)s
        result = connectToMySQL(cls.my_db).query_db(query, user_data)
        print(result)
        return result


# run find all officials
