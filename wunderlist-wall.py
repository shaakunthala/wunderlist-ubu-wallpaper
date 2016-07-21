#!/usr/bin/python

import urllib2, json, time, datetime, sys, os, PIL

from shutil import copyfile

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from pprint import pprint


a = sys.argv
homedir = os.path.expanduser('~')
try:
  a[1]
except IndexError:
  pass
else:
  # Copy the provided file
  source_file = a[1]
  try:
    copyfile (source_file, homedir + "/.wunderlist-wall/wallpaper.original")
    print ("Wallpaper replaced.")
  except IOError:
    print ("I/O error. Unable to copy the provided file ' " + source_file + " '.")
    quit (1)

# Visit https://developer.wunderlist.com/apps to find these values.
client_id = ""
access_token = ""

print "Quering task lists..."
req = urllib2.Request ('https://a.wunderlist.com/api/v1/lists', headers = {'X-Access-Token' : access_token, 'X-Client-ID' : client_id})
rsp = urllib2.urlopen (req)
lists_str = rsp.read ()
lists_json = json.loads (lists_str)

tasks_array_overdue = []
tasks_array_today = []
for tasklist in lists_json:
  if (tasklist['type'] == 'list'):
    list_title = tasklist['title']
    list_id = tasklist['id']
    
    print "Quering list items in \"" + list_title + "\""
    t_req = urllib2.Request ('https://a.wunderlist.com/api/v1/tasks?list_id=' + str(list_id), headers = {'X-Access-Token' : access_token, 'X-Client-ID' : client_id})
    t_rsp = urllib2.urlopen (t_req)
    tasks_str = t_rsp.read ()
    tasks_json = json.loads (tasks_str)
    
    for task in tasks_json:
      try:
        duedate_str = task['due_date']
      except KeyError:
        pass
      else:
        taskname = task['title']
        # print duedate_str, "          ", taskname
        
        today_str = time.strftime ('%Y-%m-%d')
        duedate_obj = datetime.datetime.strptime (duedate_str, '%Y-%m-%d').date()
        today_obj = datetime.datetime.strptime (today_str, '%Y-%m-%d').date()
        
        # Here we create an array of tasks found. 0 is when task is due today. 1 is when task is overdue.
        ctask = []
        if (duedate_str == today_str):
          # print "Today:", taskname
          ctask = [0, list_title, taskname]
        elif (duedate_obj < today_obj):
          # print "Overdue:", taskname
          ctask = [1, list_title, taskname]
        if (ctask != []):
          if (ctask[0] == 0):
            tasks_array_today.append (ctask)
          else:
            tasks_array_overdue.append (ctask)

# Now, let's sort and process the array
tasks_array_today.sort ()
tasks_array_overdue.sort ()

# Now the image processing part. Draw text on the wallpaper.
wp = Image.open (homedir + "/.wunderlist-wall/wallpaper.original")
# Understand the image geometry
wp_w = wp.width
wp_h = wp.height

# Undertand the understand the drawing geometry
# Top right
# 60% of width
# 100% of height, but keep margin for menubar
menubar_padding = (24 + 50) # Hardcoded menubar size in px + some padding
x_crd = wp_w * 0.6
y_crd = menubar_padding
# Font size 40, Ubuntu works for 878 px height image
# Let's make that a scale.
f_size = int (round ((float (30) / float (880)) * wp_h))

# Define fonts
fh = ImageFont.truetype ("Ubuntu-B.ttf", f_size, 0, "unic") # Bold
fsh = ImageFont.truetype ("Ubuntu-RI.ttf", f_size, 0, "unic") # Italic
ft = ImageFont.truetype ("Ubuntu-R.ttf", f_size, 0, "unic") # Regular

# Draw
d = ImageDraw.Draw (wp)
header = "Wunderlist Today"
d.text ((x_crd, y_crd), header, (0, 0, 0), font=fh)
next_line = fh.getsize (header)[1]
d = ImageDraw.Draw (wp)

# Overdue
if (len (tasks_array_overdue) != 0):
  header = "Overdue"
  y_crd = y_crd + next_line + 15
  d.text ((x_crd, y_crd), header, (255, 0, 0), font=fsh)
  next_line = fh.getsize (header)[1]
  d = ImageDraw.Draw (wp)
  for t in tasks_array_overdue:
    print t[1], t[2]
    if (t[0] == 1): # Overdue tasks first
      y_crd = y_crd + next_line + 10
      current_line = t[1] + " :: " + t[2]
      d.text ((x_crd, y_crd), current_line, (0, 0, 0), font=ft)
      next_line = ft.getsize (current_line)[1]
      d = ImageDraw.Draw (wp)

# Today
if (len (tasks_array_today) != 0):
  header = "Today"
  y_crd = y_crd + next_line + 15
  d.text ((x_crd, y_crd), header, (255, 255, 0), font=fsh)
  next_line = fh.getsize (header)[1]
  d = ImageDraw.Draw (wp)
  for t in tasks_array_today:
    print t[1], t[2]
    if (t[0] == 0): # Today's tasks now
      y_crd = y_crd + next_line + 10
      current_line = t[1] + " :: " + t[2]
      d.text ((x_crd, y_crd), current_line, (0, 0, 0), font=ft)
      next_line = ft.getsize (current_line)[1]
      d = ImageDraw.Draw (wp)

wp.save (homedir + "/.wunderlist-wall/wallpaper.processed", "PNG")

# Set new wallpaper
# gsettings set org.gnome.desktop.background picture-uri "file:////usr/share/backgrounds/warty-final-ubuntu.png"
os.system ("gsettings set org.gnome.desktop.background picture-uri \"file://" + homedir + "/.wunderlist-wall/wallpaper.processed\"")

print ("Done.\n")


