from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.Official_models import Official
from flask_app.models.Post_models import Post
from flask_app.models.api_models import twitter_scrape, get_congress_members, create_official_and_posts

@app.route('/officials/<int:official_id>')
def show_official(official_id):
    officials = Official.find_all_officials()
    all_states_set = set()

    for official in officials:
        official_state = official.state[:2]  # Using slicing for the first two characters
        if (official_state == 'US'):
            continue
        all_states_set.add(official_state)

        all_states_list = sorted(list(all_states_set))
    official = Official.find_official_by_id(official_id)
    print(official.first_name)
    posts = Post.get_posts_by_id(official_id)
    post_images = {}
    if (posts == False):
        return redirect('/noComment/' + str(official_id))
    for post in posts:
        post_images[post.id] = Post.get_post_images(post.id)
    if posts == False:
        return redirect('/noComment/' + str(official_id))
    return render_template('official.html', posts = posts, official = official, all_states = all_states_list, officials = officials, post_images = post_images)

@app.route('/noComment/<int:official_id>')
def no_comment(official_id):
    officials = Official.find_all_officials()
    all_states_set = set()

    for official in officials:
        official_state = official.state[:2]
        if (official_state == 'US'):
            continue
        all_states_set.add(official_state)

        all_states_list = sorted(list(all_states_set))
    official = Official.find_official_by_id(official_id)
    return render_template('noComment.html', official = official, all_states = all_states_list, officials = officials)

# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/validate_login', methods=['POST'])
# def validate_login():
#     if not Official.validate_login(request.form):
#         return redirect('/login')
#     return redirect('/officials')
