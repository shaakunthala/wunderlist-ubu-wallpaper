# Wunderlist Today in Ubuntu Wallpaper
## ATTENTION
This project has some pending work. It is not ready for regular personal use, and may require some additonal work if you set it up on your computer. Just look at the steps below - there are too many - means there's still some work to do before making this official. :)
## Introduction
**Wunderlist Today in Ubuntu Wallpaper** is a simple Python script that will update your Ubuntu wallpaper with today's tasks in Wunderlist. Tasks will appear on the top right of wallpaper.
Current state work is only suitable for use with light colour wallpapers, because I couln't figure out a way to make text visibility better than this yet.

**Disclaimer: This work is not officially affiliated with Wunderlist Gmbh. or Microsoft Corporation.**
## How to use
* Download the file `wunderlist-wall.py`.
* Visit https://developer.wunderlist.com/apps to set up a client ID and an access token.
* Edit the file `wunderlist-wall.py` and set values for `client_id` and `access_token` variables (lines 31 & 32).
* Create directory `~/.wunderslit-wall`.
* Create directory `~/bin` if you don't have it, and then copy our Python script into that.
* Make our Python script executable by doing `chmod +x ~/bin/wunderlist-wall.py`.
* Execute `wunderlist-wall.py <path to source wallpaper of choice>`. This is a one-time step. Example: `wunderlist-wall.py /usr/share/backgrounds/warty-final-ubuntu.png`
* Run the same command without any parameters (`./wunderlist-wall.py`). This should change your wallpaper. Set this up as a cronjob (`crontab -e`) to periodically query and update wallpaper.
