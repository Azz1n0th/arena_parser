#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The Projections Object is used to store data for the projections of a Movie Object.

Projections data:

- Date
- Time
- Features - represents the attributes in the div with class="attr secondary"

When calling a Projections Object, the time variable is returned.

To get all the information stored in a projection use get_projections() method of the class.
"""


class Projections:

    def __init__(self, date=None, time=None, features=None):
        self.date = date
        self.time = time
        self.features = features

    def __str__(self):
        return self.time

    def get_projections(self):
        return self.__dict__
