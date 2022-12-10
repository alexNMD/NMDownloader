from flask import current_app, render_template, redirect, request, abort
from flask_httpauth import HTTPBasicAuth
from flask_paginate import Pagination, get_page_parameter
from scripts.downloader import downloader
from tools.tools import get_list
# from scrapper import parse_data
from mongoapi import MongoAPI
from bson.objectid import ObjectId
import requests
import html
import re
import datetime
import json

mongoapi = MongoAPI()
auth = HTTPBasicAuth()

with open("static/src/etc/userdb.json") as userdb:
    users = json.load(userdb)

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            users[username] == password:
        return username


@current_app.route('/')
def racine():
    return redirect('/movies')

@current_app.route('/home')
def home():
    response = { 'status': 'OK', 'file': False }

    return render_template('index.html', response=response)

@current_app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    file = downloader(url)

    response = {}
    if file:
        response = { 'status': 'OK', 'file': file }
    else:
        response = { 'status': 'error', 'file': file }
    
    return render_template('index.html', response=response)


@current_app.route('/movies', methods=['GET'])
# @current_app.route('/movies/page/<int:page>', methods=['GET'])
def view_movies():
    title = request.args.get('search')
    genre = request.args.get('genre')
    genres = mongoapi.get_all_data("genres")
    genres = sorted(genres, key=lambda k: k['label'])

    active_link = mongoapi.get_active_link()

    page = request.args.get(get_page_parameter(), type=int, default=1)

    if not title and not genre:
        title = ""
        data, total = mongoapi.get_all_videos("movies", page - 1)
    elif title:
        data, total = mongoapi.search_videos("movies", title, "by_title", page - 1)
    elif genre:
        title = ""
        data, total = mongoapi.search_videos("movies", genre, "by_genre", page - 1)

    display_message = '''<b>{start} - {end}</b> sur un total de <b>{total}</b> {record_name}'''

    pagination = Pagination(
        page=page, 
        total=total, 
        per_page=32, 
        record_name='films', 
        css_framework='bootstrap4', 
        display_msg=display_message,
        alignment='center')

    return render_template('movies.html', data=data, search=title, genres=genres, pagination=pagination, active_link=active_link)

@current_app.route('/series', methods=['GET'])
def series():
    title = request.args.get('search')
    # genre = request.args.get('genre')
    # genres = mongoapi.get_all_data("genres")
    # genres = sorted(genres, key=lambda k: k['label'])

    # active_link = mongoapi.get_active_link()

    page = request.args.get(get_page_parameter(), type=int, default=1)

    if not title:
        title = ""
        data, total = mongoapi.get_all_videos("series", page - 1)
    elif title:
        data, total = mongoapi.search_videos("series", title, "by_title", page - 1)
    # elif genre:
    #     title = ""
    #     data, total = mongoapi.search_videos(genre, "by_genre", page - 1)

    display_message = '''<b>{start} - {end}</b> sur un total de <b>{total}</b> {record_name}'''

    pagination = Pagination(
        page=page, 
        total=total, 
        per_page=32, 
        record_name='séries', 
        css_framework='bootstrap4', 
        display_msg=display_message,
        alignment='center')

    # return render_template('movies.html', data=data, search=title, genres=genres, pagination=pagination, active_link=active_link)
    return render_template('series.html', data=data, search=title, pagination=pagination)

@current_app.route('/movie_views/<string:id>', methods=['GET'])
def movie_views(id):
    try:
        data = mongoapi.get_data({ '_id': ObjectId(id) }, 'movies')
        stream_link = data['link'].split('/')
        stream_link = stream_link[3]

        return render_template('movie_views.html', data=data, link=stream_link)
    except:
        abort(404)

@current_app.route('/serie_views/<string:id>', methods=['GET'])
def serie_views(id):
    # try:  
    data = mongoapi.get_data({ '_id': ObjectId(id) }, 'series')
    season = request.args.get('season')
    if not season:
        season = "1"

    # stream_link = data['link'].split('/')
    # stream_link = stream_link[3]

    return render_template('serie_views.html', data=data, nbseason=season)
    # except:
    #     abort(404)



@current_app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@current_app.route('/admin', methods=['GET', 'POST'])
def admin():
    # TODO: connexion au service (obligatoire)
    # TODO: visibilité sur les différents systèmes de logs (scrapper & uptader)
    # TODO: possibilité de manager les différentes infos sur la bdd

    # action = request.form.get('action')
    # if action:
        # try:
        #     # TODO: trouver une autre méthode pour automatiser (a external api maybe?)
        #     task_scheduler(parse_data)
        #     current_app.config['NMD_launcher'] = action
        # except Exception as e:
        #     print(e)
    #     current_app.apscheduler.add_job(func=bonjour, trigger='date', interval="2 minuts")
    # actual_status = current_app.config['NMD_launcher']

    return render_template('admin.html')

@current_app.route('/add-newsletter', methods=['POST'])
def add_newsletter():
    email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    # name = html.escape(request.form.get('name'))
    email = html.escape(request.form.get('email'))

    data = {
        # "name": name,
        "email": email
    }
    if re.search(email_regex, email) and not mongoapi.get_data({'email': email}, 'mailing_list'):
        mongoapi.insert_data(data, "mailing_list")
    else:
        return redirect('/movies?newsletter_status=error')

    return redirect('/movies?newsletter_status=success')

@current_app.route('/series', methods=['POST'])
@auth.login_required
def add_series():
    data = request.json
    requiredFields = ["Title", "genre", "links", "Poster", "season"]

    try:
        serie = {
            "Title": data['title'],
            "genre": data['genres'],
            "added_at": datetime.datetime.now(),
            "seasons": { 
                f"{ data['season'] }": {
                    "season_number:" : int(data['season']),
                    "links": data['links'] 
                }
            },
            "Poster": data['poster']
        }
        mongoapi.insert_data(serie, "series")
        return { "message": "Added successfully !"}, 200
    except:
        return { "message": "Format error !" }, 400


@current_app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
# defining function 
  return render_template("404.html"), 404


