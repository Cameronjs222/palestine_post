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
print(congress_key)
# Create your models here.


# Initialize the ApifyClient with your API token
client = ApifyClient(token=apify_key)

def twitter_scrape(official, date):
    output = []
# Prepare the Actor input
    run_input = {
            "max_tweets": 500,
            "language": "any",
            "use_experimental_scraper": False,
            "user_info": "user info and replying info",
            "max_attempts": 5,
            "newer_than": date,
            "from_user": [official]
        }

        # Run the Actor and wait for it to finish
    run = client.actor("wHMoznVs94gOcxcZl").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        try:
            output.append(item)
        except UnicodeEncodeError:
            continue
    return output

def create_official_and_posts(officials_list):
    for official_data in officials_list:        
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
        
        posts = twitter_scrape(twitter_handle, "2023-10-07")
        for post in posts:
            post_data = {
                'post_avatar': post['post_avatar'],
                'url': post['url'],
                'query': post['query'],
                'post_id': post['post_id'],
                'text': post['text'],
                'username': post['username'],
                'fullname': post['fullname'],
                'timestamp': post['timestamp'],
                'replies': post['replies'],
                'reposts': post['reposts'],
                'likes': post['likes'],
                'quotes': post['quotes']
            }

            try:
                post_id = post.create_post(post_data, official_id)
                print(f"post created with ID: {post_id}")
                
                if len(post['images']) > 0:
                    for image in post['images']:
                        image_data = {'image_url': image}
                        post.add_post_images(image_data, post_id)
                        print(f"Image added to post")
            except Exception as e:
                print(f"Error creating post: {str(e)}")
    
    return "posts created"


def get_congress_members(congress, chamber):
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

# Example usage
congress_number = "116"
chamber_type = "house"

result = get_congress_members(congress_number, chamber_type)

if result:
    print(result)
    
    
