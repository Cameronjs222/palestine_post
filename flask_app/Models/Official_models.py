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
    def __init__(self, id=None, official_id=None, title=None, short_title=None,
                api_uri=None, first_name=None, middle_name=None, last_name=None,
                suffix=None, date_of_birth=None, gender=None, party=None,
                twitter_account=None, facebook_account=None, youtube_account=None,
                govtrack_id=None, cspan_id=None, votesmart_id=None, icpsr_id=None,
                crp_id=None, google_entity_id=None, fec_candidate_id=None, url=None,
                rss_url=None, contact_form=None, in_office=None, cook_pvi=None,
                dw_nominate=None, ideal_point=None, seniority=None, next_election=None,
                total_votes=None, missed_votes=None, total_present=None,
                last_updated=None, ocd_id=None, office=None, phone=None, fax=None,
                state=None, district=None, missed_votes_pct=None,
                votes_with_party_pct=None, votes_against_party_pct=None,
                at_large=None, geoid=None):
        self.id = id
        self.official_id = official_id
        self.title = title
        self.short_title = short_title
        self.api_uri = api_uri
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.suffix = suffix
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.party = party
        self.twitter_account = twitter_account
        self.facebook_account = facebook_account
        self.youtube_account = youtube_account
        self.govtrack_id = govtrack_id
        self.cspan_id = cspan_id
        self.votesmart_id = votesmart_id
        self.icpsr_id = icpsr_id
        self.crp_id = crp_id
        self.google_entity_id = google_entity_id
        self.fec_candidate_id = fec_candidate_id
        self.url = url
        self.rss_url = rss_url
        self.contact_form = contact_form
        self.in_office = in_office
        self.cook_pvi = cook_pvi
        self.dw_nominate = dw_nominate
        self.ideal_point = ideal_point
        self.seniority = seniority
        self.next_election = next_election
        self.total_votes = total_votes
        self.missed_votes = missed_votes
        self.total_present = total_present
        self.last_updated = last_updated
        self.ocd_id = ocd_id
        self.office = office
        self.phone = phone
        self.fax = fax
        self.state = state
        self.district = district
        self.at_large = at_large
        self.geoid = geoid
        self.missed_votes_pct = missed_votes_pct
        self.votes_with_party_pct = votes_with_party_pct
        self.votes_against_party_pct = votes_against_party_pct
        self.post = None

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'twitter_handle': self.twitter_handle,
            'state': self.state,
            'district': self.district,
            'post': self.post,
            'official_id': self.official_id,
            'title': self.title,
            'short_title': self.short_title,
            'api_uri': self.api_uri,
            'middle_name': self.middle_name,
            'suffix': self.suffix,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'party': self.party,
            'twitter_account': self.twitter_account,
            'facebook_account': self.facebook_account,
            'youtube_account': self.youtube_account,
            'govtrack_id': self.govtrack_id,
            'cspan_id': self.cspan_id,
            'votesmart_id': self.votesmart_id,
            'icpsr_id': self.icpsr_id,
            'crp_id': self.crp_id,
            'google_entity_id': self.google_entity_id,
            'fec_candidate_id': self.fec_candidate_id,
            'url': self.url,
            'rss_url': self.rss_url,
            'contact_form': self.contact_form,
            'in_office': self.in_office,
            'cook_pvi': self.cook_pvi,
            'dw_nominate': self.dw_nominate,
            'ideal_point': self.ideal_point,
            'seniority': self.seniority,
            'next_election': self.next_election,
            'total_votes': self.total_votes,
            'missed_votes': self.missed_votes,
            'total_present': self.total_present,
            'last_updated': self.last_updated,
            'ocd_id': self.ocd_id,
            'office': self.office,
            'phone': self.phone,
            'fax': self.fax,
            'at_large': self.at_large,
            'geoid': self.geoid,
            'missed_votes_pct': self.missed_votes_pct,
            'votes_with_party_pct': self.votes_with_party_pct,
        }


    @classmethod
    def find_official_by_id(cls, id):
        query = """
        SELECT * FROM officials WHERE id = %(id)s
        """

        data = {
            'id': id
        }

        results = connectToMySQL(cls.my_db).query_db(query, data)
        official = Official(id=results[0]['id'], first_name=results[0]['first_name'], last_name=results[0]['last_name'], twitter_account=results[0]['twitter_handle'], state=results[0]['state'], district=results[0]['district'])
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
        officials = []
        for official in results:
            try:
                official_post = Post.get_post_by_id(official['id'])
                official = Official(id=official['id'], first_name=official['first_name'], last_name=official['last_name'], twitter_account=official['twitter_handle'], state=official['state'], district=official['district'])
                official.post = official_post
                officials.append(official)
            except:
                continue
        return officials
    @classmethod
    def find_official_by_name(cls, first_name, last_name):
        query = """
        SELECT * FROM officials WHERE first_name = %(first_name)s AND last_name = %(last_name)s
        """

        data = {
            'first_name': first_name,
            'last_name': last_name
        }

        results = connectToMySQL(cls.my_db).query_db(query, data)
        officials = []
        for official in results:
            try:
                official = Official(id=official['id'], first_name=official['first_name'], last_name=official['last_name'], twitter_account=official['twitter_handle'], state=official['state'], district=official['district'])
                officials.append(official)
            except:
                continue
        
        return official
    
    @classmethod
    def find_officials_by_state(cls, state):
        query = """
        SELECT * FROM officials WHERE state like %(state)s
        """

        data = {
            'state': f'%%{state}%%',
        }

        results = connectToMySQL(cls.my_db).query_db(query, data)
        officials = []
        for official in results:
            try:
                official = Official(id=official['id'], first_name=official['first_name'], last_name=official['last_name'], twitter_account=official['twitter_handle'], state=official['state'], district=official['district'])
                officials.append(official)
            except:
                continue

        return officials
    @classmethod
    def find_all_officials_with_post(cls):
        query = """
        SELECT * FROM officials
        """
        results = connectToMySQL(cls.my_db).query_db(query)
        officials = []
        for result in results:
            try:
                official_post = Post.get_post_by_id(result['id'])
                official = Official(id=result['id'], first_name=result['first_name'], last_name=result['last_name'], twitter_account=result['twitter_handle'], state=result['state'], district=result['district'])
                official.post = official_post
                print(type(official.post))
                officials.append(official)
            except:
                continue

        return officials
    
    @classmethod
    def find_all_officials(cls):
        query = """
        SELECT * FROM officials
        """
        results = connectToMySQL(cls.my_db).query_db(query)
        officials = []
        for result in results:
            official = Official(id=result['id'], first_name=result['first_name'], last_name=result['last_name'], twitter_account=result['twitter_handle'], state=result['state'], district=result['district'])
            print(official.id)
            officials.append(official)

        return officials
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
    
    @staticmethod
    def get_congress_members(congress, chamber):
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