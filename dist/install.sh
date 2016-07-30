#!/bin/bash

if [[ `whoami` == "root" ]]; then
  echo "+++++++++++++++++++"
  echo "Are you sure to run this as root? This may cause unexpected results."
  echo "Press Ctrl + C to exit. Press Enter to continue if you think it's okay."
  echo "+++++++++++++++++++"
  read
fi

mydir=`dirname $0`
initial_bg="/usr/share/backgrounds/warty-final-ubuntu.png"

echo ""
echo "============================================="
echo "Wunderlist Today in Ubuntu Desktop Background"
echo "============================================="
echo ""
echo "Installer: Please select an option."
echo "    [1] Install"
echo "    [2] Remove"
echo "    [3] Re-install"
echo "    [0] Quit"
echo ""

while read -p "How do you want to proceed? " -n 1 c && [ "$c" -gt 3 ]; do
echo ""
echo "Invalid choice. Please choose between 0, 1, 2, 3."
done
echo ""

case $c in
  0)
    echo "Ok, quitting..."
    exit
    ;;
  1)
    echo "Installing the script for current user `whoami`."
    mkdir "$HOME/bin" 2> /dev/null
    cp -i "$mydir/wunderlist-bg.py" "$HOME/bin/wunderlist-bg.py"
    chmod 700 "$HOME/bin/wunderlist-bg.py"
    mkdir "$HOME/.wunderlist-bg" 2> /dev/null
    # Authentication secrets - prompt user to enter.
    # Initial wallpaper
    read -p "Please enter the full path to initial background image [default: $initial_bg]: " bg_image
    if [[ "$bg_image" == "" ]]; then
      bg_image="$initial_bg"
      $HOME/wunderlist-bg.py $bg_image
    fi
    # Set the cronjob
    # Set here
    echo "Cronjob set: "
    crontab -l | grep "wunderlist-bg.py"
    ;;
  2)
    echo "Removing the script from current user `whoami`."
    rm -f "$HOME/bin/wunderlist-bg.py"
    rm -rf "$HOME/.wunderlist-bg"
    # Remove crontab
    echo "Done."
    ;;
  3)
    echo "Re-installing"
    ;;
esac
