# Wunderlist Today in Ubuntu Desktop Background
## What's New (13 August 2016)
* Padding for menubar will now calculate depending on background image size. Earlier it was a hardcoded value (24 + 50 = 74 px). Now it is partially hardcoded (calculation based on 24 px).
* No more cron. Now script is wait and repeat itself. Installation steps simplified and more customizable by changing the `wait_time` variable (in seconds). In a future update I'll make this easily configurable. PLEASE read through "How to use" section once again if you are already using this.

## ATTENTION
This project has some pending work. It is not ready for regular personal use, and may require some additonal work if you set it up on your computer. Just look at the steps below - there are too many - means there's still some work to do before making this official. :)
## Introduction
**Wunderlist Today in Ubuntu Desktop Background** is a simple Python script that will update your Ubuntu dekstop background with today's tasks in Wunderlist. Tasks will appear on the top right of the chosen image.
Current state work is only suitable for use with light colour backgrounds, because I couln't figure out a way to make text visibility better than this yet.

**Disclaimer: This work is not officially affiliated with Wunderlist Gmbh. or Microsoft Corporation.**
## How to use
* Download the files `wunderlist-bg.py` and `wunderlist-bg-startup.py`.
* Visit https://developer.wunderlist.com/apps to set up a client ID and an access token.
* Edit the file `wunderlist-bg.py` and set values for `client_id` and `access_token` variables (lines 4 & 5).
* Create directory `~/.wunderslit-wall`.
* Create directory `~/bin` if you don't have it, and then copy our two Python scripts into that.
* Make our Python scripts executable by doing `chmod +x ~/bin/wunderlist-bg.py ~/bin/wunderlist-bg-startup.py`.
* Execute `wunderlist-bg.py <path to source image of choice>`. This is a one-time step. Example: `wunderlist-bg.py /usr/share/backgrounds/warty-final-ubuntu.png`
* Run the same command following `nohup`, but without any parameters (`nohup ./wunderlist-bg.py &> /dev/null`). This should change your desktop background.
* Set to run automatically with session startup. Execute `gnome-session-properties`. Add a new startup program by clicking Add button. Name: Wunderlist Today background. Command: `/usr/bin/python /home/<username>/bin/wunderlist-bg-startup.py` (PAY ATTENTION to the filename here). It will start working with your next session start.

### Important if you have previously set up a cronjob
* Execute `crontab -e` and delete the line which executes `wunderlist-bg.py`.

## Changelog
### 30 July 2016
* Changed the project name. Renamed script - replaced word 'wallpaper' by 'background' because it is more appropriate with Ubuntu.
* Changed application settings directory accordingly. Updated this file accordingly.
* An installer script is being created.

### 25 July 2016
* Eliminated the additional copy of source image file. Instead, introduced a settings file that will keep a hash of the previous run.
* If Today's list hasn't changed since the previous run, image processing will not take place. This eliminates unnecessary I/O overhead.

### 26 July 2016
* Processed image will now be saved to /tmp and then be overwritten into the background image copy in `~/.wunderlist-bg`. This will reduce the blackout time during background image udate.
* Image saving is now optimized, and it will use PNG compression level 9.
