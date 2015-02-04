#!/usr/bin/env python
# dhtdb.py
# mikeder 2015

import requests
import datetime
import sqlite3
import os

cwd = os.path.dirname(os.path.realpath(__file__))
dbpath = cwd + '/data/dht.db'
r = requests.get('http://192.168.1.20')
tempC = int(r.json()[u'tempC'])
tempF = int(r.json()[u'tempF'])
humidity = int(r.json()[u'humidity'])


# Create database if it doesn't exist
def createDB():
  sql = '''
        CREATE TABLE IF NOT EXISTS
          data(id INTEGER PRIMARY KEY,
          date DATETIME,
          tempC INTEGER,
          tempF INTEGER,
          humidity INTEGER)'''
  db = sqlite3.connect(dbpath)
  cursor = db.cursor()
  cursor.execute(sql)
  db.commit()
  db.close()

# Update database with new data
def updateDB(tempC, tempF, humidity):
  date = datetime.datetime.now()
  sql = '''
        INSERT INTO data(date, tempC, tempF, humidity)
        VALUES(?,?,?,?)'''
  data = [(date,tempC,tempF,humidity)]
  db = sqlite3.connect(dbpath)
  cursor = db.cursor()
  cursor.executemany(sql,data)
  db.commit()
  db.close()

if __name__ == "__main__":

  print('** DHT Poller/DB Updater **')
  print('Check database')
  if os.path.isfile(dbpath):
    print('OK')
  else:
    createDB()
    print('Database created')
  try:
    updateDB(tempC, tempF, humidity)
  except Exception as e:
    print('Error while updating database')
    print(e)
  print('Current readings:')
  print('Temperature C: %d' % tempC)
  print('Temperature F: %d' % tempF)
  print('Humidity: %d' % humidity)
