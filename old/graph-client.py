#!/usr/bin/python
"""Copyright 2008 Orbitz WorldWide

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import sys
import time
import os
import platform
import requests
import subprocess
from socket import socket

CARBON_SERVER = 'graphite'
CARBON_PORT = 2003

delay = 60 
if len(sys.argv) > 1:
  delay = int( sys.argv[1] )

def get_climate():
  r = requests.get('http://192.168.1.20')
  tC = int(r.json()[u'tempC'])
  tF = int(r.json()[u'tempF'])
  h = int(r.json()[u'humidity'])
  return(tC, tF, h)

def get_loadavg():
  # For more details, "man proc" and "man uptime"  
  if platform.system() == "Linux":
    return open('/proc/loadavg').read().strip().split()[:3]
  else:   
    command = "uptime"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    os.waitpid(process.pid, 0)
    output = process.stdout.read().replace(',', ' ').strip().split()
    length = len(output)
    return output[length - 3:length]

sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)

while True:
  now = int( time.time() )
  lines = []
  #We're gonna report all three loadavg values
  loadavg = get_loadavg()
  # Get new values from DHT sensor
  tC, tF, h = get_climate()
  lines.append("tools.loadavg_1min %s %d" % (loadavg[0],now))
  lines.append("tools.loadavg_5min %s %d" % (loadavg[1],now))
  lines.append("tools.loadavg_15min %s %d" % (loadavg[2],now))
  lines.append("dht.tempC %d %d" % (tC, now))
  lines.append("dht.tempF %d %d" % (tF, now))
  lines.append("dht.hum %d %d" % (h, now))
  message = '\n'.join(lines) + '\n' #all lines must end in a newline
  print "sending message\n"
  print '-' * 80
  print message
  print
  sock.sendall(message)
  time.sleep(delay)
