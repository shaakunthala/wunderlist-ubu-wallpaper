#!/usr/bin/python

import time, os, sys

a = sys.argv
wait_time = 900

try:
  a[1]
except IndexError:
  pass
else:
  try:
    wait_time = int(a[1]) * 60
  except ValueError:
    wait_time = 900
  else:
    wait_time = int(a[1]) * 60

while True:
  print ("WRAPPER: STARTING ITERATION")
  os.system ("wunderlist-bg.py")  
  print ("WRAPPER: WAITING " + str (wait_time) + " SECONDS")
  time.sleep (wait_time)
  
