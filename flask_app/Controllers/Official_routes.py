from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.Models.Official_models import Official

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

@app.route('/officials/new', methods = ['POST'])
def new_official():
    senate = Official.get_congress_members(117, 'senate')
    house = Official.get_congress_members(117, 'house')
    print(senate)
    for member in senate['results'][0]['members']:
        Official.create_official(member)
    for member in house['results'][0]['members']:
        Official.create_official(member)
    return render_template("index.html")