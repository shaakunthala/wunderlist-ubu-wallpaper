#!/usr/bin/python

import time, os

wait_time = 900

while True:
  print ("WRAPPER: STARTING ITERATION")
  os.system ("wunderlist-bg.py")  
  print ("WRAPPER: WAITING " + str (wait_time) + " SECONDS")
  time.sleep (wait_time)
  
