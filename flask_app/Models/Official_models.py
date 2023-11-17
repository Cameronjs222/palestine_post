from flask_app.Config.mysqlconnection import connectToMySQL
from flask_app.Models.Post_models import Post
from apify_client import ApifyClient
import requests
import configparser
import os
# Load the API key from the .env file
config = configparser.ConfigParser()
config.read('config.ini')

# apify_key = os.g('apify_api_key')
# congress_key = os.getenv('congress_api_key')
apify_key = config['API_KEYS']['APIFY_API_KEY']
congress_key = config['API_KEYS']['CONGRESS_API_KEY']
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
        self.phone = None
        self.post = []

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
    def find_official_by_id(cls, id):
        query = """
        SELECT * FROM officials WHERE id = %(id)s
        """

        data = {
            'id': id
        }

        results = connectToMySQL(cls.my_db).query_db(query, data)
        for official in results:
            official = Official(official['id'], official['first_name'], official['last_name'], official['twitter_handle'], official['state'], official['district'])
            return official
        return official
    @classmethod
    def find_official_by_id_with_post(cls, id):
        query = """
        SELECT * FROM officials WHERE id = %(id)s
        """

        data = {
            'id': id
        }

        results = connectToMySQL(cls.my_db).query_db(query, data)
        for official in results:
            official_post = Post.get_post_by_id(official['id'])
            official = Official(official['id'], official['first_name'], official['last_name'], official['twitter_handle'], official['state'], official['district'])
            official.post = official_post
            print(type(official.post))
            return official
        return official
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
    def find_officials_by_state(cls, state):
        query = """
        SELECT * FROM officials WHERE state like %(state)s
        """

        data = {
            'state': f'%%{state}%%',
        }

        return connectToMySQL(cls.my_db).query_db(query, data)
    @classmethod
    def find_all_officials_with_post(cls):
        query = """
        SELECT * FROM officials
        """
        results = connectToMySQL(cls.my_db).query_db(query)
        list_of_officials = []
        for result in results:
            official_post = Post.get_post_by_id(result['id'])
            official = Official(result['id'], result['first_name'], result['last_name'], result['twitter_handle'], result['state'], result['district'])
            official.post = official_post
            print(type(official.post))
            list_of_officials.append(official)

        return list_of_officials
    
    @classmethod
    def find_all_officials(cls):
        query = """
        SELECT * FROM officials
        """
        results = connectToMySQL(cls.my_db).query_db(query)
        print(results)
        list_of_officials = []
        for result in results:
            official = Official(result['id'], result['first_name'], result['last_name'], result['twitter_handle'], result['state'], result['district'])
            list_of_officials.append(official)

        return list_of_officials
    @classmethod
    def create_official(cls, member):
        query = """
            INSERT INTO your_table_name (
                official_id, title, short_title, api_uri, first_name, middle_name, last_name, suffix,
                date_of_birth, gender, party, twitter_account, facebook_account, youtube_account,
                govtrack_id, cspan_id, votesmart_id, icpsr_id, crp_id, google_entity_id,
                fec_candidate_id, url, rss_url, contact_form, in_office, cook_pvi, dw_nominate,
                ideal_point, seniority, next_election, total_votes, missed_votes, total_present,
                last_updated, ocd_id, office, phone, fax, state, district, at_large, geoid,
                missed_votes_pct, votes_with_party_pct, votes_against_party_pct, at_large, geoid
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Extract values from the member data
        data = (
            member['id'], member['title'], member['short_title'], member['api_uri'],
            member['first_name'], member['middle_name'], member['last_name'], member['suffix'],
            member['date_of_birth'], member['gender'], member['party'], member['twitter_account'],
            member['facebook_account'], member['youtube_account'], member['govtrack_id'],
            member['cspan_id'], member['votesmart_id'], member['icpsr_id'], member['crp_id'],
            member['google_entity_id'], member['fec_candidate_id'], member['url'],
            member['rss_url'], member['contact_form'], member['in_office'], member['cook_pvi'],
            member['dw_nominate'], member['ideal_point'], member['seniority'], member['next_election'],
            member['total_votes'], member['missed_votes'], member['total_present'],
            member['last_updated'], member['ocd_id'], member['office'], member['phone'],
            member['fax'], member['state'], member['district'], member['at_large'], member['geoid'],
            member['missed_votes_pct'], member['votes_with_party_pct'], member['votes_against_party_pct'], member['at_large'], member['geoid']
        )
        result = connectToMySQL(cls.my_db).query_db(query, data)
        print(result)
        return result
    
    @classmethod
    def get_congress_members(cls, congress, chamber):
        print(congress_key)
        """
        Get a list of members for a particular chamber in a specific Congress.

        Args:
        - congress (str): The Congress number (e.g., "116").
        - chamber (str): The chamber ("house" or "senate").
        - api_key (str): Your ProPublica API key.

        Returns:
        - dict: JSON response containing information about members.
        """
        base_url = "https://api.propublica.org/congress/v1"
        endpoint = f"/{congress}/{chamber}/members.json"
        url = f"{base_url}{endpoint}"

        headers = {"X-API-Key": congress_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
        return None