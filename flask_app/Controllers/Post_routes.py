from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.Models.Official_models import Official
from flask_app.Models.Post_models import Post

@app.route('/officials/<int:official_id>')
def show_official(official_id):
    posts = Post.get_posts_by_id(official_id)
    if posts == False:
        return redirect('/officials')
    return render_template('official.html', posts = posts)
