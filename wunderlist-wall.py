#!/usr/bin/python

# Visit https://developer.wunderlist.com/apps to find these values.
client_id = ""
access_token = ""

import urllib2, json, time, datetime, sys, os, hashlib, ConfigParser, PIL

from ConfigParser import SafeConfigParser

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from pprint import pprint

# TODO:
# Check for any exiting instances of the script and kill them before execution.


# Save settings function
def savesettings (config, pref_file):
  with open(pref_file, 'w') as sf:
    config.write (sf)
  return True
  
# Load settings function
def loadsettings (pref_file):
  config = SafeConfigParser()
  config.read (pref_file)
  return config

a = sys.argv
homedir = os.path.expanduser('~')
appdir = homedir + "/.wunderlist-wall"
infile= ""
outfile = appdir + "/wallpaper"
settingsfile = appdir + "/settings"
override_skip = False
force_write_settings = False

default_wallpaper = "/usr/share/backgrounds/warty-final-ubuntu.png"

# Read settings file, and if there's none, create one with default settings.
try:
  open (settingsfile, 'a').close ()
  conf = loadsettings (settingsfile)
except:
  print ("Settings error. Re-creating settings file...")
  open (settingsfile, 'w').close ()


# Read config
try:
  conf.get ("main", "src_file")
except ConfigParser.NoSectionError:
  print ("Creating a new settings file with default Ubuntu wallpaper.")
  conf.add_section ("main")
  conf.set ("main", "src_file", default_wallpaper)
  force_write_settings = True
except ConfigParser.NoOptionError:
  conf.set ("main", "src_file", default_wallpaper)
  force_write_settings = True

try:
  conf.get ("main", "last_run")
except ConfigParser.NoOptionError:
  conf.set ("main", "last_run", "")

infile = conf.get ("main", "src_file")
last_run = conf.get ("main", "last_run")


# Check if new setting provided by command line parameter
try:
  a[1]
except IndexError:
  pass
else:
  if (infile != a[1]):
    conf.set ("main", "src_file", a[1])
    infile = a[1]
    override_skip = True
    print ("Wallpaper replaced.")
  else:
    print ("Already using this wallpaper.")
    

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

# Compare task list hash arrays and stop if no update is required. This is to reduce I/O overhead.
current_run = str (hashlib.sha1 (str (tasks_array_today)).hexdigest ()) + "::" + str (hashlib.sha1 (str (tasks_array_overdue)).hexdigest ())
if (override_skip == False):
  if (last_run == current_run):
    # Do not continue. Save setting if forced file and exit.
    if (force_write_settings == True):
      savesettings (conf, settingsfile)
    print ("Task list hasn't changed since the last run. Nothing to do.")
    quit ()
  else:
    conf.set ("main", "last_run", current_run)
conf.set ("main", "last_run", current_run)

# Now the image processing part. Draw text on the wallpaper.
wp = Image.open (infile)
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

wp.save (outfile, "PNG")

# Set new wallpaper
os.system ("gsettings set org.gnome.desktop.background picture-uri \"file://" + outfile + "\"")

print ("Saving settings...")

savesettings (conf, settingsfile)

print ("Done.\n")



