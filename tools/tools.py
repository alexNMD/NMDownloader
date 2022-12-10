import os
import requests
import smtplib
import json
from datetime import datetime
from mongoapi import MongoAPI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
mongoapi = MongoAPI()


email_sender = "alexnmd@alwaysdata.net"
email_sender_pwd = "xxxxxxxxxx"

# def launch_download(url):
#     # filename = time.time()
#     # mon_fichier = requests.get(url)
#     # open(f'downloads/{ filename }', 'wb').write(mon_fichier.content)

#     return False

def get_list():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'downloads/')
    files = os.listdir(path)
    data = []

    for file in files:
        size = os.path.getsize(f"{path}/{file}")
        size = size_filter(size)
        data.append({'name': file, 'size': size })

    return data


def size_filter(size):
    letters = ''

    if len(str(size)) <= 5:
        size /= 1000
        letters = 'Ko'
    elif len(str(size)) <= 8:
        size /= 1000000
        letters = 'Mo'
    elif len(str(size)) <= 10:
        size /= 1000000000
        letters = 'Go'

    size = round(size, 2)
    size = f"{str(size)} {letters}"

    return size

# def get_email_template(data):
#     body = render_template("email-template.html", data=data)

#     return body


def send_message(data):
    mailing_list = mongoapi.get_mailing_list()
    msg = MIMEMultipart()
    msg['From'] = email_sender
    # msg['Bcc'] = ", ".join(mailing_list)
    msg['Bcc'] = "ale.normand@icloud.com"
    msg['Subject'] = 'Newsletter - The NMDownloader' 
    # message = "films ajoutés : \n" + str(data)

    try:
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)

        template = env.get_template('email-template.html')
        message = template.render(data=data)

        msg.attach(MIMEText(message, 'html'))



        mailserver = smtplib.SMTP('smtp-alexnmd.alwaysdata.net', 25)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(email_sender, email_sender_pwd)
        mailserver.sendmail(email_sender, mailing_list, msg.as_string())
        mailserver.quit()
    except:
        pass



def logger(content, type: int):
    log_assoc = {
        0: "scrapper_logs",
        1: "link_updated_logs"
    }
    filename = log_assoc[type]
    today = datetime.now().today().strftime("%d-%m-%Y_%H:%M:%S")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    file_object = open(f'{path}/logs/{filename}.txt', 'a')

    line = f"{today} - {content}"

    file_object.write(f"{line} \n")
 
    # Close the file
    file_object.close()


# def get_genre():
#     from bs4 import BeautifulSoup
#     data = mongoapi.get_all_movies()
#     collection = mongoapi.get_collection('movies')

#     for d in data:
#         print(d['Title'])
#         content = requests.get(d['base_url']).content
#         soup = BeautifulSoup(content, "html.parser")

#         for under_line in soup.find_all('u'):
#             if under_line.text == "Genre":
#                 genres = under_line.next_element.next_element.next_element
#                 genres = genres.split(',')
#                 genres = [x for x in genres if x != ' ']
#                 genres = [x for x in genres if x != '\n']
#                 genres = [x.lower().strip() for x in genres]

#                 for genre in genres:
#                     if not mongoapi.get_data({'label': genre}, "genres"):
#                         mongoapi.insert_data({'label': genre}, "genres")

#                 collection.find_one_and_update({'_id': d['_id']}, {'$set': {'genre': genres}})

# print(get_genre())
