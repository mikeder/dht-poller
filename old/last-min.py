#!/usr/bin/env python
# current.py
# mikeder 2015

import pygal
import sqlite3
import datetime
import os
from pygal.style import LightenStyle
dark_lighten_style = LightenStyle('#ADD658', step=5)
degreeF = u"\u2109"
degreeC = u"\u2103"
percent = u"\u0025"
cwd = os.path.dirname(os.path.realpath(__file__))
dbpath = cwd + '/data/dht.db'
db = sqlite3.connect(dbpath)
cur = db.cursor()
sql = '''
      SELECT * FROM data order by id desc limit 1
      '''
db.row_factory = sqlite3.Row 
cur.execute(sql)
row = cur.fetchone()
time = row[1]
tempC = row[2]
tempF = row[3]
humidity = row[4]

chart = pygal.Bar(human_readable=True,
                    width=400,
                    height=200,
                    label_font_size=12,
                    )
chart.title = 'Temperature and Humidity - Current'
chart.range = [0, 100]
chart.add('Temp ' + degreeF, tempF)
chart.add('Temp ' + degreeC, tempC)
chart.add('Humidity ' + percent, humidity)
chart.render_to_file('current.svg')
