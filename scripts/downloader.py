import requests
import time
import re

url = "http://www92.uptobox.com/dl/phrjFWQJ_WqNCJ1gHE2vgxoFPehZ8mk50eQGgW4QxfdbucbaS2d6W22evl_g-YcTBTJEI9dnEIn8B6jzqcywI4Nflkclyn2DHkqOyNrcwP5PplmWZaM4tU8hPuY4qF8dGOY7Ipn4cGvpL0kCXLgaCg/upload.zip"
episode_regex = "[A-Z][0-5][0-9][A-Z][0-5][0-9]"



def rename_movie(movie):
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
        return new_string
    except:
        pass

def rename_episode(episode):
    words = episode.split('.')
    format = '.' + words[len(words)-1]
    new_string = ""

    for word in words:
        if (bool(re.search(episode_regex, word))):
            episode_index = words.index(word)

    try:
        del words[episode_index + 1:len(words)]

        for i, word in enumerate(words):
            if i != 0:
                new_string = new_string + " " + word
            else:
                new_string += word

        new_string += format
        return new_string
    except:
        pass



def downloader(url):
    name = ''
    try:
        url_list = url.split('/')
        filename = url_list[len(url_list) - 1]
        if (bool(re.search(episode_regex, filename))):
            name = rename_episode(filename)
        else:
            name = rename_movie(filename)
        # TODO: faire le downloader
        return name
    except:
        return False