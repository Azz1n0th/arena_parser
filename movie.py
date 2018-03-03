#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The movie object should represent a movie and be stored in a cinema object.

It contains the following information:

- Movie Title(taken from the title in the html->head tag of the movie page)
- Description(taken from the article with class content)
- Link to the cover image
- A dictionary with genre, length, director etc. organized with key: value pairs
- Projections(a list of projections for a movie)

The string representation of the Movie object is the movie title.

Use Movie(url).__dict__ or the class' get_movie() method to get the dictionary of the Movie object.

Add more documentation!

"""

import urllib3
from bs4 import BeautifulSoup
from datetime import datetime
start = datetime.now()
http = urllib3.PoolManager()
home = 'http://www.kinoarena.com'


class Movie:

    all_movies = dict()

    def __init__(self, url):
        self.url = url
        self._movie_title = None
        self._description = None
        self._image_link = None
        self._reported = dict()
        self.projections = list()

    def __str__(self):
        return self._movie_title

    def load_movie(self, movie_list_name):
        if movie_list_name not in Movie.all_movies.keys():
            page = http.request('GET', self.url)
            soup = BeautifulSoup(page.data, 'html.parser')
            self._movie_title = soup.title.text[:soup.title.text.find('|')].strip().strip()
            self._description = soup.find('article', attrs={'class': 'content'}).text.strip('\n')
            self._image_link = home + soup.find('img', attrs={'title': self._movie_title})['src']
            for item in soup.find('div', attrs={'class': 'report'}):
                child = BeautifulSoup(str(item), 'html.parser')
                key = child.find(attrs={'class': 'name'})
                value = child.find(attrs={'class': 'value'})
                if key is not None and value is not None:
                    self._reported[key.text] = value.text
            Movie.all_movies[self._movie_title] = self.__dict__
        else:
            self.__dict__ = Movie.all_movies[movie_list_name]

    def get_movie(self):
        return self.__dict__
