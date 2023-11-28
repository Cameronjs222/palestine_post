from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.Models.Official_models import Official
from flask_app.Models.Post_models import Post
from flask_app.Models.api_models import twitter_scrape, get_congress_members, create_official_and_posts

@app.route('/officials/<int:official_id>')
def show_official(official_id):
    official = Official.find_official_by_id(official_id)
    print(official.first_name)
    posts = Post.get_posts_by_id(official_id)
    if posts == False:
        return redirect('/noComment/' + str(official_id))
    return render_template('official.html', posts = posts, official = official)

@app.route('/noComment/<int:official_id>')
def no_comment(official_id):
    official = Official.find_official_by_id(official_id)
    return render_template('noComment.html', official = official)