"""
  The Cinema Object should be given a URL to the cinema page to start scraping.

  This is a class for handling a cinema object containing:
  - name
  - description
  - address
  - phone
  - email
  - dictionary of movies with references: key = movie_name; value = movie_object

  The __init__ method works with a couple of local variables to be able to set the object
  variables. The only parameter passed to the Movie object should be the movie URL.

  A call to the Cinema Object will return the Cinema Name.

  Use cinema.__dict__ to get the object dictionary! Alternatively use the get_cinema_dict() method
  of the Cinema Object.
  """

import urllib3
from bs4 import BeautifulSoup
from lib.movie import Movie
import datetime
import json
import time

current_year = datetime.datetime.now().year
home = "http://kinoarena.com"
http = urllib3.PoolManager()


class Cinema:

    def __init__(self, url):
        self.cinema_url = url
        self._name = None
        self._description = None
        self._address = None
        self._phone = None
        self._email = None
        self._movies = dict()
        self.__page = http.request('GET', self.cinema_url)
        self._movies_url = self.cinema_url + '/movies'

    def __str__(self):
        return self.__dict__['_name']

    def get_all_movies(self):
        movies_page = http.request('GET', self._movies_url)
        if movies_page.status == 200:
            local_soup = BeautifulSoup(movies_page.data, 'html.parser')
            return local_soup.find_all(attrs={'class': 'contentWrapper'})
        else:
            raise ConnectionError("Movies Page is not found.")

    def add_all_movies(self):
        local_http = http.request('GET', self._movies_url)
        date = BeautifulSoup(local_http.data, 'html.parser').find('a', attrs={'class': 'selected'}).text[:5]
        year = str(date) + "." + str(current_year)
        for movie in self.get_all_movies():
            local_soup = BeautifulSoup(str(movie), 'html.parser')
            movie_name = local_soup.find('h5').text

            try:
                self._movies[movie_name]['projections']
            except KeyError:
                if movie_name in Movie.all_movies:
                    self._movies[movie_name] = Movie.all_movies[movie_name]
                else:
                    time.sleep(10)
                    movie = Movie(url=home + local_soup.a['href'])
                    movie.load_movie(movie_name)
                    self._movies[str(movie)] = movie.__dict__

            row = local_soup.find_all('div', attrs={'class': 'row'})
            for current in row:
                mini_soup = BeautifulSoup(str(current), 'html.parser')
                attributes = []
                for image in mini_soup.find_all('img'):
                    if image['alt']:
                        attributes.append(image['alt'])
                if attributes:
                    for item in current.find('div', attrs={'class': 'timelineSet'}).text.split():
                        try:
                            self._movies[str(movie)]['projections'].append({
                                'features': attributes,
                                'projection': item,
                                'date': year
                            })
                        except KeyError:
                            self._movies[movie_name]['projections'].append({
                                'features': attributes,
                                'projection': item,
                                'date': year
                            })

    def get_dates(self):
        local_soup = BeautifulSoup(self.__page.data,
                                   'html.parser').find(attrs={'class':
                                                              'stenikTabsHeader'}).find_all('a')
        dates = []
        for item in local_soup:
            dates.append(home + item['href'])
        return dates

    def add_cinema(self):
        self.__page = http.request('GET', self.cinema_url)
        if self.__page.status is 200:
            soup = BeautifulSoup(self.__page.data, 'html.parser')
            details = soup.find_all('div', attrs={'class': 'circleButton'})
            details = BeautifulSoup(str(details), 'html.parser').find_all('p')

            self._name = soup.find('h1').text
            self._description = soup.find('div',
                                          attrs={'class': 'content'}).text.replace('\n', " ").replace('\xa0', ' ')
            self._address = soup.find('div', attrs={'class': 'secondaryTxt'}).text.strip('\n')
            self._phone = details[1].text.replace(" ", '')
            self._email = details[2].text
            self._movies_url = self.cinema_url + '/movies'
            self._movies = dict()

            for_dates = http.request('GET', self.cinema_url + '/movies').data

            for date in BeautifulSoup(for_dates, 'html.parser').find_all(attrs={'class': 'tabItem'}):
                self._movies_url = home + date['href']
                self.add_all_movies()
        else:
            raise ValueError("Page not found")
        self.__page = None

    def get_cinema_dict(self):
        return self.__dict__
