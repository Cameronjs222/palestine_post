from flask_app.Config.mysqlconnection import connectToMySQL
from flask_app.Models.Post_models import Post
from apify_client import ApifyClient
from config import congress_api_key
import requests
import configparser
import os
# Create your models here.

class Official():
    my_db = 'palestine_tweets'
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
    def find_officials_by_name(cls, first_name, last_name):
        query = """
        SELECT * FROM officials WHERE first_name LIKE %(first_name)s AND last_name LIKE %(last_name)s
        """

        data = {
            'first_name': f"%%{first_name}%%",
            'last_name': f"%%{last_name}%%"
        }

        results = connectToMySQL(cls.my_db).query_db(query, data)
        print(results)
        officials = []
        if results:
            print("found officials")
            for official_data in results:
                official = Official(
                    id= official_data.get('id', None),
                    official_id= official_data.get('official_id', None),
                    title= official_data.get('title', None),
                    short_title= official_data.get('short_title', None),
                    api_uri= official_data.get('api_uri', None),
                    first_name= official_data.get('first_name', None),
                    middle_name= official_data.get('middle_name', None),
                    last_name= official_data.get('last_name', None),
                    suffix= official_data.get('suffix', None),
                    date_of_birth= official_data.get('date_of_birth', None),
                    gender= official_data.get('gender', None),
                    party= official_data.get('party', None),
                    twitter_account= official_data.get('twitter_handle', None),
                    facebook_account= official_data.get('facebook_account', None),
                    youtube_account= official_data.get('youtube_account', None),
                    govtrack_id= official_data.get('govtrack_id', None),
                    cspan_id= official_data.get('cspan_id', None),
                    votesmart_id= official_data.get('votesmart_id', None),
                    icpsr_id= official_data.get('icpsr_id', None),
                    crp_id= official_data.get('crp_id', None),
                    google_entity_id= official_data.get('google_entity_id', None),
                    fec_candidate_id= official_data.get('fec_candidate_id', None),
                    url= official_data.get('url', None),
                    rss_url= official_data.get('rss_url', None),
                    contact_form= official_data.get('contact_form', None),
                    in_office= official_data.get('in_office', None),
                    cook_pvi= official_data.get('cook_pvi', None),
                    dw_nominate= official_data.get('dw_nominate', None),
                    ideal_point= official_data.get('ideal_point', None),
                    seniority= official_data.get('seniority', None),
                    next_election= official_data.get('next_election', None),
                    total_votes= official_data.get('total_votes', None),
                    missed_votes= official_data.get('missed_votes', None),
                    total_present= official_data.get('total_present', None),
                    last_updated= official_data.get('last_updated', None),
                    ocd_id= official_data.get('ocd_id', None),
                    office= official_data.get('office', None),
                    phone= official_data.get('phone', None),
                    fax= official_data.get('fax', None),
                    state= official_data.get('state', None),
                    district= official_data.get('district', None),
                    missed_votes_pct= official_data.get('missed_votes_pct', None),
                    votes_with_party_pct= official_data.get('votes_with_party_pct', None),
                    votes_against_party_pct= official_data.get('votes_against_party_pct', None),
                    at_large= official_data.get('at_large', None),
                    geoid= official_data.get('geoid', None)
                    )
                officials.append(official)
            print(officials, " officials")
            return officials
        else:
            return False
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
            INSERT INTO officials (
                official_id, title, short_title, api_uri, first_name, middle_name, last_name, suffix,
                date_of_birth, gender,

                party, twitter_handle, facebook_account, youtube_account,
                govtrack_id, cspan_id, votesmart_id, icpsr_id, crp_id, google_entity_id,

                fec_candidate_id, url, rss_url, contact_form, in_office, cook_pvi, dw_nominate,
                ideal_point, seniority, next_election,

                total_votes, missed_votes, total_present,
                last_updated, ocd_id, office, phone, fax, state, district,

                missed_votes_pct, votes_with_party_pct, votes_against_party_pct, at_large, geoid) 
                
                VALUES (%(official_id)s, %(title)s, %(short_title)s, %(api_uri)s, %(first_name)s, %(middle_name)s, %(last_name)s, %(suffix)s,
                %(date_of_birth)s, %(gender)s, 
                
                %(party)s, %(twitter_handle)s, %(facebook_account)s, %(youtube_account)s,
                %(govtrack_id)s, %(cspan_id)s, %(votesmart_id)s, %(icpsr_id)s, %(crp_id)s, %(google_entity_id)s,
                
                %(fec_candidate_id)s, %(url)s, %(rss_url)s, %(contact_form)s, %(in_office)s, %(cook_pvi)s, %(dw_nominate)s,
                %(ideal_point)s, %(seniority)s, %(next_election)s, 
                
                %(total_votes)s, %(missed_votes)s, %(total_present)s,
                %(last_updated)s, %(ocd_id)s, %(office)s, %(phone)s, %(fax)s, %(state)s, %(district)s, 
                
                %(missed_votes_pct)s, %(votes_with_party_pct)s, %(votes_against_party_pct)s, %(at_large)s, %(geoid)s)
        """

        # Extract values from the member data
        data = {
        'official_id': member.get('id', None),
        'title': member.get('title', None),
        'short_title': member.get('short_title', None),
        'api_uri': member.get('api_uri', None),
        'first_name': member.get('first_name', None),
        'middle_name': member.get('middle_name', None),
        'last_name': member.get('last_name', None),
        'suffix': member.get('suffix', None),
        'date_of_birth': member.get('date_of_birth', None),
        'gender': member.get('gender', None),
        'party': member.get('party', None),
        'twitter_handle': member.get('twitter_account', None),
        'facebook_account': member.get('facebook_account', None),
        'youtube_account': member.get('youtube_account', None),
        'govtrack_id': member.get('govtrack_id', None),
        'cspan_id': member.get('cspan_id', None),
        'votesmart_id': member.get('votesmart_id', None),
        'icpsr_id': member.get('icpsr_id', None),
        'crp_id': member.get('crp_id', None),
        'google_entity_id': member.get('google_entity_id', None),
        'fec_candidate_id': member.get('fec_candidate_id', None),
        'url': member.get('url', None),
        'rss_url': member.get('rss_url', None),
        'contact_form': member.get('contact_form', None),
        'in_office': member.get('in_office', None),
        'cook_pvi': member.get('cook_pvi', None),
        'dw_nominate': member.get('dw_nominate', None),
        'ideal_point': member.get('ideal_point', None),
        'seniority': member.get('seniority', None),
        'next_election': member.get('next_election', None),
        'total_votes': member.get('total_votes', None),
        'missed_votes': member.get('missed_votes', None),
        'total_present': member.get('total_present', None),
        'last_updated': member.get('last_updated', None),
        'ocd_id': member.get('ocd_id', None),
        'office': member.get('office', None),
        'phone': member.get('phone', None),
        'fax': member.get('fax', None),
        'state': member.get('state', None),
        'district': member.get('district', None),
        'missed_votes_pct': member.get('missed_votes_pct', None),
        'votes_with_party_pct': member.get('votes_with_party_pct', None),
        'votes_against_party_pct': member.get('votes_against_party_pct', None),
        'at_large': member.get('at_large', None),
        'geoid': member.get('geoid', None)
        }

        result = connectToMySQL(cls.my_db).query_db(query, data)
        print(result, "result")
        return result
    
    @classmethod
    def update_official(cls, member, id):
        query = """
UPDATE officials
SET 
    official_id = %(official_id)s, 
    title = %(title)s, 
    short_title = %(short_title)s, 
    api_uri = %(api_uri)s, 
    first_name = %(first_name)s, 
    middle_name = %(middle_name)s, 
    last_name = %(last_name)s, 
    suffix = %(suffix)s,
    date_of_birth = %(date_of_birth)s, 
    gender = %(gender)s,

    party = %(party)s, 
    twitter_handle = %(twitter_handle)s, 
    facebook_account = %(facebook_account)s, 
    youtube_account = %(youtube_account)s,
    govtrack_id = %(govtrack_id)s, 
    cspan_id = %(cspan_id)s, 
    votesmart_id = %(votesmart_id)s, 
    icpsr_id = %(icpsr_id)s, 
    crp_id = %(crp_id)s, 
    google_entity_id = %(google_entity_id)s,

    fec_candidate_id = %(fec_candidate_id)s, 
    url = %(url)s, 
    rss_url = %(rss_url)s, 
    contact_form = %(contact_form)s, 
    in_office = %(in_office)s, 
    cook_pvi = %(cook_pvi)s, 
    dw_nominate = %(dw_nominate)s,
    ideal_point = %(ideal_point)s, 
    seniority = %(seniority)s, 
    next_election = %(next_election)s,

    total_votes = %(total_votes)s, 
    missed_votes = %(missed_votes)s, 
    total_present = %(total_present)s,
    last_updated = %(last_updated)s, 
    ocd_id = %(ocd_id)s, 
    office = %(office)s, 
    phone = %(phone)s, 
    fax = %(fax)s, 
    state = %(state)s, 
    district = %(district)s,

    missed_votes_pct = %(missed_votes_pct)s, 
    votes_with_party_pct = %(votes_with_party_pct)s, 
    votes_against_party_pct = %(votes_against_party_pct)s, 
    at_large = %(at_large)s, 
    geoid = %(geoid)s
WHERE official_id = %(id)s;
        """

        # Extract values from the member data
        data = {
        'official_id': member.get('id', None),
        'title': member.get('title', None),
        'short_title': member.get('short_title', None),
        'api_uri': member.get('api_uri', None),
        'first_name': member.get('first_name', None),
        'middle_name': member.get('middle_name', None),
        'last_name': member.get('last_name', None),
        'suffix': member.get('suffix', None),
        'date_of_birth': member.get('date_of_birth', None),
        'gender': member.get('gender', None),
        'party': member.get('party', None),
        'twitter_handle': member.get('twitter_account', None),
        'facebook_account': member.get('facebook_account', None),
        'youtube_account': member.get('youtube_account', None),
        'govtrack_id': member.get('govtrack_id', None),
        'cspan_id': member.get('cspan_id', None),
        'votesmart_id': member.get('votesmart_id', None),
        'icpsr_id': member.get('icpsr_id', None),
        'crp_id': member.get('crp_id', None),
        'google_entity_id': member.get('google_entity_id', None),
        'fec_candidate_id': member.get('fec_candidate_id', None),
        'url': member.get('url', None),
        'rss_url': member.get('rss_url', None),
        'contact_form': member.get('contact_form', None),
        'in_office': member.get('in_office', None),
        'cook_pvi': member.get('cook_pvi', None),
        'dw_nominate': member.get('dw_nominate', None),
        'ideal_point': member.get('ideal_point', None),
        'seniority': member.get('seniority', None),
        'next_election': member.get('next_election', None),
        'total_votes': member.get('total_votes', None),
        'missed_votes': member.get('missed_votes', None),
        'total_present': member.get('total_present', None),
        'last_updated': member.get('last_updated', None),
        'ocd_id': member.get('ocd_id', None),
        'office': member.get('office', None),
        'phone': member.get('phone', None),
        'fax': member.get('fax', None),
        'state': member.get('state', None),
        'district': member.get('district', None),
        'missed_votes_pct': member.get('missed_votes_pct', None),
        'votes_with_party_pct': member.get('votes_with_party_pct', None),
        'votes_against_party_pct': member.get('votes_against_party_pct', None),
        'at_large': member.get('at_large', None),
        'geoid': member.get('geoid', None),
        'id': int(id)
        }
    
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