#!/usr/bin/env python
# last24.py
# mikeder 2015

import pygal
import sqlite3
import datetime
import os
from pygal.style import LightenStyle
dark_lighten_style = LightenStyle('#ADD658', step=5)

cwd = os.path.dirname(os.path.realpath(__file__))
dbpath = cwd + '/data/dht.db'
db = sqlite3.connect(dbpath)
cur = db.cursor()
sql = '''
      SELECT * FROM data WHERE date >= 
      datetime('now', '-1 day')
      '''
db.row_factory = sqlite3.Row 
cur.execute(sql)
rows = cur.fetchall()
db.close()
time = []
tempC = []
tempF = []
humidity = []
degreeF = u"\u2109"
degreeC = u"\u2103"
percent = u"\u0025"
for item in rows:
  time.append(item[1])
  tempC.append(item[2])
  tempF.append(item[3])
  humidity.append(item[4])
# Flast
flast = [time[0], time[1]]
# Alternate every 5
def altElement(a):
  return a[::5]
chart = pygal.Line(interpolate='cubic',
                   dots_size=.5,
                   range=(0,100),
                   show_dots=True,
                   label_font_size=12,
                   show_minor_x_labels=False,
                   x_label_rotation=45,
                   truncate_label=20,
                   style=dark_lighten_style)
chart.title = 'Temperature and Humidity - Past 24hrs'
chart.x_labels = altElement(time)
chart.x_labels_major = flast
chart.add('Temp ' + degreeF, altElement(tempF))
chart.add('Temp ' + degreeC, altElement(tempC))
chart.add('Humidity ' + percent, altElement(humidity))
chart.render_to_file('last24.svg')
