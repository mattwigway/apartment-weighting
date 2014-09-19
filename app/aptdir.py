#!/usr/bin/python

import json
from flask import Flask, request
from urllib2 import urlopen
from urllib import urlencode
from db import *

app = Flask(__name__)

# Persist this through the session
# ugly ugly ugly ugly
apts = []

# Perform a Craigslist search and save it in the database
@app.route('/search', method='POST')
def search():
    # e.g. roo for shared rooms, apt for apartments
    typ = request.form['type']
    search = request.form['search']

    assert typ in ['roo', 'apt']

    # make the request
    res = json.loads(urlopen('http://washingtondc.craigslist.org/jsonsearch/%s/%s' %
                             (typ, urlencode(dict(query=search, sale_date='-')))))


    for apt in res:
        a = Apartment()
        # Just store lat/lon here as that's what OTP uses internally anyhow
        a.lon = float(apt['Longitude'])
        a.lat = float(apt['Latitude'])
        a.url = apt['PostingURL']
        a.title = apt['PostingTitle']
        a.date = int(apt['PostedDate'])
        a.price = int(apt['Ask'])
        apts.append(a)
