# Wunderlist Today in Ubuntu Wallpaper
## What's New (26 June 2016)
* Processed image will now be saved to /tmp and then be overwritten into the wallpaper copy in `~/.wunderlist-wall`. This will reduce the blackout time during wallpaper udate.
* Image saving is now optimized, and it will use PNG compression level 9.

## ATTENTION
This project has some pending work. It is not ready for regular personal use, and may require some additonal work if you set it up on your computer. Just look at the steps below - there are too many - means there's still some work to do before making this official. :)
## Introduction
**Wunderlist Today in Ubuntu Wallpaper** is a simple Python script that will update your Ubuntu wallpaper with today's tasks in Wunderlist. Tasks will appear on the top right of wallpaper.
Current state work is only suitable for use with light colour wallpapers, because I couln't figure out a way to make text visibility better than this yet.

**Disclaimer: This work is not officially affiliated with Wunderlist Gmbh. or Microsoft Corporation.**
## How to use
* Download the file `wunderlist-bg.py`.
* Visit https://developer.wunderlist.com/apps to set up a client ID and an access token.
* Edit the file `wunderlist-bg.py` and set values for `client_id` and `access_token` variables (lines 4 & 5).
* Create directory `~/.wunderslit-wall`.
* Create directory `~/bin` if you don't have it, and then copy our Python script into that.
* Make our Python script executable by doing `chmod +x ~/bin/wunderlist-bg.py`.
* Execute `wunderlist-bg.py <path to source wallpaper of choice>`. This is a one-time step. Example: `wunderlist-bg.py /usr/share/backgrounds/warty-final-ubuntu.png`
* Run the same command without any parameters (`./wunderlist-bg.py`). This should change your wallpaper. Set this up as a cronjob (`crontab -e`) to periodically query and update wallpaper. (Example: `0,15,30,45 * * * *	/usr/bin/python /home/ushaasa/bin/wunderlist-bg.py`)

## Changelog
### 25 June 2016
* Eliminated the additional copy of source image file. Instead, introduced a settings file that will keep a hash of the previous run.
* If Today's list hasn't changed since the previous run, image processing will not take place. This eliminates unnecessary I/O overhead.
