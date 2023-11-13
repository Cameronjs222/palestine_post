from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.Models.Official_models import Official

@app.route('/')
def index():
    # officials = Official.find_all_officials()
    return render_template("search.html")