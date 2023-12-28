import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask_app.models.api_models import twitter_scrape
from flask_app.models.Official_models import Official
from flask_app import app
from flask import render_template, redirect, request, session, flash

@app.route('/official/twitter/update/test', methods=['POST', 'GET'])
def update_twitter_test():
    print(request.form)
    date = request.form['date']
    limit = int(request.form['limit'])
    congress_limit = int(request.form['congress_limit'])
    test_congress = Official.find_all_officials()[:congress_limit]

    if test_congress:
        # Use ThreadPoolExecutor to parallelize API calls
        with ThreadPoolExecutor() as executor:
            # Use list comprehension to submit tasks
            futures = [executor.submit(twitter_scrape, member.twitter_account, date, limit) for member in test_congress]
        # Wait for all tasks to complete using as_completed
        for completed_future in as_completed(futures):
            try:
                result = completed_future.result()
                # Handle the result (result is assumed to be an array of dictionaries)
                print(result)
            except Exception as e:
                # Handle exceptions if any occurred during the execution of the task
                print(f"An error occurred: {e}")

    return "done"
