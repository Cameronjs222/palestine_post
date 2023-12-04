from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.Models.Official_models import Official
from flask_app.Models.Post_models import Post
from flask_app.Models.api_models import twitter_scrape, get_congress_members, create_official_and_posts
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor, as_completed

import concurrent.futures

@app.route('/admin')
def admin():
    return render_template("index.html")
@app.route('/')
def index():
    officials = Official.find_all_officials()
    all_states_set = set()

    for official in officials:
        official_state = official.state[:2]  # Using slicing for the first two characters
        if (official_state == 'US'):
            continue
        all_states_set.add(official_state)

        all_states_list = sorted(list(all_states_set))
        count = len(all_states_list)

    print(all_states_list)
    print(count)
    return render_template("search.html" , officials = officials, all_states = all_states_list, count = count)

@app.route('/states/<state>')
def show_state(state):
    officials = Official.find_officials_by_state(state)
    print(officials)
    return render_template("states.html", officials = officials)

@app.route('/official/congress/get', methods=['POST', 'GET'])
def get_congress():
    print(request.form)
    try:
        congress = int(request.form['select_term'])
        chamber = request.form['select_chamber']
        full_congress = get_congress_members(congress, chamber)
        print(full_congress)
        if full_congress:
            for member in full_congress['results'][0]['members']:
                member['last_updated'] = member['last_updated'][:10]
                official_id = Official.find_officials_by_name(member['first_name'], member['last_name'])
                if official_id:
                    print(official_id)
                    for member_id in official_id:
                        Official.update_official(member, member_id.id)
                else:
                    print(member)
                    Official.create_official(member)
        return redirect(f'/admin?congress={congress}&chamber={chamber}&full_congress=True')
    except KeyError as e:
        print("KeyError " + str(e))
        chamber = request.form['select_chamber']
        return redirect(f'/admin?chamber={chamber}&full_congress=False')
    except ValueError as e:
        print("ValueError" + str(e))
        # Handle the case where 'select_term' cannot be converted to an integer
        return redirect('/admin?full_congress=False')

@app.route('/official/twitter/update', methods=['POST', 'GET'])
def update_twitter():
    print(request.form)
    date = request.form['date']
    limit = int(request.form['limit'])
    congress_limit = int(request.form['congress_limit'])
    full_congress = Official.find_all_officials()[:congress_limit]

    if full_congress:
        # Use ThreadPoolExecutor to parallelize API calls
        with ThreadPoolExecutor() as executor:
            # Use list comprehension to submit tasks
            futures = [
                executor.submit(process_member, member, date, limit) for member in full_congress
            ]

    return "done"



def process_member(member, date, limit):
    try:
        # Call twitter_scrape and capture the result
        tweets = twitter_scrape(member.twitter_account, date, limit)
        
        for tweet in tweets:
            print(f"Processing tweet: {tweet['post_id']}, user: {tweet['username']}")
            post_data = {
                'post_avatar': tweet['post_avatar'],
                'url': tweet['url'],
                'query': tweet['query'],
                'post_id': tweet['post_id'],
                'text': tweet['text'],
                'username': tweet['username'],
                'fullname': tweet['fullname'],
                'timestamp': tweet['timestamp'],
                'replies': tweet['replies'],
                'reposts': tweet['reposts'],
                'likes': tweet['likes'],
                'quotes': tweet['quotes'],
                'official_id': member.id,
            }

            try:
                print(f"Creating post for {member.first_name} {member.last_name}")
                post_id = Post.create_post(post_data, member.id)
                print(f"post created with ID: {post_id}")
                
                if len(tweet['images']) > 0:
                    print(f"Adding images to post for {member.first_name} {member.last_name}")
                    for image in tweet['images']:
                        image_data = {'image_url': image}
                        Post.add_post_images(image_data, post_id)
                        print(f"Image added to post")
            except Exception as e:
                print(f"Error creating post: {str(e)}")
        
        return {"success": True, "member_id": member.id}
    except Exception as e:
        return {"success": False, "member_id": member.id, "error": str(e)}
