import os
from flask import Flask, request, jsonify
from twitter_scraper import Profile, get_tweets

app = Flask(__name__)
secret = os.getenv('SECRET', '1234')


@app.route('/')
def index():
    return 'it works!'


@app.route('/profile/<account>')
def profile(account=None):

    if 'Authorization' not in request.headers or request.headers['Authorization'] != 'Basic ' + secret:
        response = jsonify({'error': 'Wrong token'})
        response.status_code = 403
        return response

    if account is None:
        response = jsonify({'error': 'Incorrect id'})
        response.status_code = 403
        return response

    try:
        tw_profile = Profile(account)
        print("ddd", tw_profile)
    except IndexError:
        response = jsonify({'error': 'ID NOT FOUND'})
        response.status_code = 404
        return response

    return jsonify(tw_profile.to_dict())


@app.route('/timeline/<account>')
def timeline(account=None):

    if 'Authorization' not in request.headers or request.headers['Authorization'] != 'Basic ' + secret:
        response = jsonify({'error': 'Wrong token'})
        response.status_code = 403
        return response

    if account is None:
        response = jsonify({'error': 'Incorrect id'})
        response.status_code = 403
        return response
        
    result = []

    for tweet in get_tweets(account, pages=5):
        result.append(tweet['text'])
    return jsonify(result)


#app.run(port=os.getenv('PORT', 5000))
