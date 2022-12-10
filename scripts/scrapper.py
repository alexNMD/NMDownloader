import requests
import os
import base64
import datetime
import sys
from bs4 import BeautifulSoup
from flask import current_app

import cfscrape
scraper = cfscrape.create_scraper(delay=10)

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(f'{path}/tools/')

from tools import logger, send_message
from mongoapi import MongoAPI

# url = 'https://www.zone-annuaire.com/'
url_films = "https://www.zone-annuaire.com/top-films/"
url_series = "https://www.zone-annuaire.com/serie-vostfr/"
url_animes = "https://www.zone-annuaire.com/animes/"


mongoapi = MongoAPI()


def get_data_url(urls):
# Récupère les différentes qualitées dispo sur le lien
    links = []

    for url in urls:
        # content = requests.get(url).content
        content = scraper.get(url).content
        soup = BeautifulSoup(content, "html.parser")

        datas = soup.find_all('div', attrs={"class": "cover_infos_title"})
        for data in datas:
            links.append(data.a['href'])

    return links


def get_download_link(url):
# Récupère le lien streaming directement chez Uptobox (ou autres..)
    provider_expected = "Uptobox"
    # content = requests.get(url).content
    content = scraper.get(url).content
    soup = BeautifulSoup(content, "html.parser")

    types_of_links = []
    for type in soup.find_all( 'font', attrs={'color': 'red'}):
        types_of_links.append(type.text)
    download_info = soup.find('div', attrs={"class": "postinfo"})


    try:
        for type in download_info.findAll('div'):
            if type.text == provider_expected:
                if type.findNext('a').text == "Télécharger":
                    link = type.findNext('a')['href']
                    break

        link = link.replace('/voirlien/', '/telecharger/')
        content = requests.get(link).content
        # content = scraper.get(url).content
        soup = BeautifulSoup(content, "html.parser")
        upto_link = soup.find('p', attrs={'class': 'showURL'})
        return upto_link.text
    except:
        return False


def get_genre(soup):

    for under_line in soup.find_all('u'):
        if under_line.text == "Genre":
            genres = under_line.next_element.next_element.next_element
            genres = genres.split(',')
            genres = [x for x in genres if x != ' ']
            genres = [x for x in genres if x != '\n']
            genres = [x.lower().strip() for x in genres]

            for genre in genres:
                if genre != "":
                    if not mongoapi.get_data({'label': genre}, "genres"):
                        mongoapi.insert_data({'label': genre}, "genres")

    try:
        genres
    except:
        genres = []

    return genres


def parse_data(urls: list = ["https://www.zone-annuaire.com/top-films/", "https://www.zone-annuaire.com/nouveaux-films/"]):
    # TODO: traiter le cas des séries et films
    urls = get_data_url(urls)
    qualities_expected = mongoapi.get_all_data('qualities_expected')
    qualities_expected = [ quality['label'] for quality in qualities_expected ]

    news = []

    for url in urls:
        # content = requests.get(url).content
        content = scraper.get(url).content
        soup = BeautifulSoup(content, "html.parser")

        versions = soup.find('div', attrs={"class": "otherversions"})
        title = soup.find('div', attrs={'class': 'smallsep'})
        title = title.findNext('div').text

        for under_line in soup.find_all('u'):
            if under_line.text == "Titre original":
                original_title = under_line.next_element.next_element.next_element

        for under_line in soup.find_all('u'):
            if under_line.text == "Date de sortie":
                release_date = under_line.next_element.next_element.next_element
        
        for under_line in soup.find_all('u'):
            if under_line.text == "Genre":
                genres = under_line.next_element.next_element.next_element
                genres = genres.split(',')
                genres = [x for x in genres if x != ' ']
                genres = [x for x in genres if x != '\n']
                genres = [x.lower().strip() for x in genres]

                for genre in genres:
                    if not mongoapi.get_data({'label': genre}, "genres"):
                        mongoapi.insert_data({'label': genre}, "genres")
        
        # Position [3] => selon mes dires
        poster = soup.find_all('img')[3]['src']
        
        
        try:
            release_date = release_date[1:5]
        except:
            release_date = ""

        if versions:
            qualities = versions.find_all('a')
            for link in qualities:
                if not mongoapi.get_data({'Title': title.upper()}, "movies"):
                # Vérification si le film n'existe pas déjà en base
                    if link.span.getText() in qualities_expected:
                        data = {}
                        data['Poster'] = poster
                        upto_link = get_download_link(f"https://www.zone-annuaire.com/film-gratuit{link['href']}")
                        if upto_link:
                            try:
                                OMDapi = requests.get(f"http://www.omdbapi.com/?apikey=2e324a0c&t={original_title}&y={release_date}").json()
                                if OMDapi['Response'] == 'True':
                                    data = OMDapi
                                    # data['link'] = upto_link
                                    # data['Title'] = title.upper()
                                    # data['genre'] = genre
                                # else:
                                    
                                    # data['genre'] = genre
                            except:
                                pass
                            
                            data['genre'] = get_genre(soup)
                            data['base_url'] = f"https://www.zone-annuaire.com/film-gratuit{link['href']}"
                            data['link'] = upto_link
                            data['Title'] = title.upper()
                            data['added_at'] = datetime.datetime.now()
                            news.append(data)
                            mongoapi.insert_data(data, "movies")

    logger(f'films recuperes : {len(news)}', 0)
    if len(news) > 0:
        send_message(news)


    return True

# unit test
# print(parse_data())
# print(parse_data(["https://www.zone-annuaire.com/film-gratuit/64756-telecharger-le-roi-lion-hdlight-1080p-multi.html"]))
# print(get_download_link('https://www.zone-annuaire.com/film-gratuit/58286-telecharger-bumblebee-bdrip-truefrench.html'))
# print(get_download_link("https://www.zone-annuaire.com/film-gratuit/64052-telecharger-john-wick-parabellum-bdrip-truefrench.html"))



def main():
    content = scraper.get("https://ed-protect.org/0g3sN4").content
    soup = BeautifulSoup(content, "html.parser")
    print(soup)



if __name__ =="__main__":
    # execute only if run as a script.
    main()