from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.Models.Official_models import Official
from flask_app.Models.api_models import twitter_scrape, get_congress_members, create_official_and_posts
from concurrent.futures import ThreadPoolExecutor
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
def create_post():
    print(request.form)
    try:
        congress = int(request.form['select_term'])
        chamber = request.form['select_chamber']
        full_congress = get_congress_members(congress, chamber)
        if full_congress:
            for member in full_congress:
                if Official.find_official_by_name(member['first_name'], member['last_name']):
                    Official.update_official(member)
                else:
                    Official.create_official(member)
        return redirect(f'/admin?congress={congress}&chamber={chamber}&full_congress=True')
    except KeyError:
        chamber = request.form['select_chamber']
        return redirect(f'/admin?chamber={chamber}&full_congress=False')
    except ValueError:
        # Handle the case where 'select_term' cannot be converted to an integer
        return redirect('/admin?full_congress=False')
    
@app.route('/official/twitter/update', methods=['POST', 'GET'])
def update_twitter():
    print(request.form)
    date = request.form['date']
    
    try:
        full_congress = Official.find_all_officials()
        if full_congress:
            # Use ThreadPoolExecutor to parallelize API calls
            with ThreadPoolExecutor() as executor:
                # Use list comprehension to submit tasks
                futures = [executor.submit(twitter_scrape, member.twitter_account, date) for member in full_congress]
                
                # Wait for all tasks to complete
                concurrent.futures.wait(futures)
            
        return redirect(f'/admin?full_congress=True')
    except KeyError:
        chamber = request.form['select_chamber']
        return redirect(f'/admin?chamber={chamber}&full_congress=False')
    except ValueError:
        # Handle the case where 'select_term' cannot be converted to an integer
        return redirect('/admin?full_congress=False')