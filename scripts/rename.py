# rename movie & episode

# ex : Ad.Astra.2019.MULTi.TRUEFRENCH.1080p.HDLight.x264.AC3-EXTREME_wWw.Extreme-Down.Xyz.mkv (movie)
# ex : The.Duel.2016.MULTI.1080p.mHD.x264.AC3-SVR-Zone-Telechargement.com.mkv (movie)
# ex : Vikings.S06E03.VOSTFR.1080p.WEB.H264-EXTREME.mkv (serie)

""" 
If movie : 
after the title, there must be a year.
Si série :
after the title, there must be a season and episode. like this: "S01E09"
how to use it :
use this command : "python ./rename.py [path of your folder]" and press enter!! enjoy!
 """

import os
import glob
import re
import sys

types = ('*.mkv', '*.mp4', '*.avi')
files = []
regex = "[A-Z][0-5][0-9][A-Z][0-5][0-9]"
path = sys.argv[1]

file_updated = 0

movies = [] # list of movies sorted
series = [] # list of series sorted


for type in types:
    files.extend(glob.glob(path + type))



for file in files:

    if len(file.split('.')) != 2:
        file_updated += 1
        if (bool(re.search(regex, file))):
            series.append(file)
        else:
            movies.append(file)


for episode in series:
    words = episode.split('.')
    format = '.' + words[len(words)-1]
    new_string = ""

    for word in words:
        if (bool(re.search(regex, word))):
            episode_index = words.index(word)

    try:
        del words[episode_index + 1:len(words)]

        for i, word in enumerate(words):
            if i != 0:
                new_string = new_string + " " + word
            else:
                new_string += word

        new_string += format
        os.rename(episode, new_string)
    except:
        pass


for movie in movies:
    words = movie.split('.')
    format = '.' + words[len(words)-1]
    new_string = ""

    for word in words:
        try:
            int(word)
            if (len(word) == 4):
                year_index = words.index(word)
        except:
            pass
    try:
        del words[year_index + 1:len(words)]

        for i, word in enumerate(words):
            if i != 0:
                new_string = new_string + " " + word
            else:
                new_string += word
        new_string += format
        os.rename(movie, new_string)
    except:
        pass

print(f"{ file_updated } file(s) updated!")