import requests
import os
import base64
import datetime
import sys
from bs4 import BeautifulSoup


path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(f'{ path }/tools/')

from tools import logger
from mongoapi import MongoAPI
from scrapper import get_download_link


mongoapi = MongoAPI()
movies = mongoapi.get_all_data("movies")

def check_is_alive(url: str):
    try:
        content = requests.get(url).content
        soup = BeautifulSoup(content, "html.parser")
        status = soup.find('h1', attrs={"class": "file-title"}).text

        if status == "File not found ":
            return False
        else:
            return True
    except:
        return False

# def update_link():
#     compteur = 0
#     for movie in movies:
#         if not check_is_alive(movie['link']):
#             newlink = get_download_link(movie['base_url'])
#             if newlink:
#                 mongoapi.update_ded_link(movie['_id'], newlink)
#                 compteur += 1
#         else:
#             pass

#     logger(f'liens mis à jour : {compteur}', 1)

collection = mongoapi.get_collection("movies")

movies = movies[::-1]
for index, movie in enumerate(movies):
        if not check_is_alive(movie['link']):
            status = False
        else:
            status = True
        collection.find_one_and_update({'_id': movie['_id']}, {'$set': { 'status': status }})
        print(f"{ index }/{ len(movies) } => { status }", end='\r')