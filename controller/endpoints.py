from flask import Blueprint, request, render_template, jsonify, send_from_directory, Response
import requests

from config import Config
from model.imdb import IMDb

endpoints = Blueprint('endpoints', __name__)
# TODO: Add CSRF protection


# @endpoints.route('/')
# def index():
#     return render_template('app/login.html')
#
#
# @endpoints.route('/login')
# def login():
#     return render_template('templates/login.html')
    # username = request.form.get('username')
    # password = request.form.get('password')
    # success = {
    #     'response': 'success'
    # }
    # fail = {
    #     'response': 'fail'
    # }
    # if username == 'ed' and password == '123':
    #     print('success')
    #     return jsonify(success)
    # else:
    #     print('fail')
    #     return jsonify(fail)
    # return jsonify(response)


@endpoints.route('/query')
def query():
    payload = {
        'apikey': Config.OMDB_API_KEY,
        'i': 'tt0133093',
        'type': 'movie',
        'page': '1',
    }
    # try:
    result = IMDb.query(Config.OMDB_URL, params=payload)
    return jsonify(result)
    # except Exception as e.:
    #     return e.__str__()


# @routes.route('/delete')
# def delete():
#     client = Config.mongo_client
#     client.imdb.registers.delete_many({})
#     return 'success'
#
#
# @routes.route('/find')
# def find():
#     client = Config.mongo_client
#     db = client.imdb
#     # result = db.posts.insert_one(
#     #     {
#     #         'title': 'The Matrix',
#     #         'type': 'movie',
#     #     }
#     # )
#
#     result = db.registers.find()
#
#     items = []
#     for r in result:
#         items.append(IMDb.remove_mongo_id(r))
#
#     return jsonify(items)
#
#
# @routes.route('/test')
# def test():
#     return 'test'