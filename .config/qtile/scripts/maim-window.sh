#! /bin/sh
maim --window $(xdotool getactivewindow) /home/slats/Images/Screenshots/$(date +%Y-%b-%d--%H-%M-%S_maim | tr A-Z a-z).png
notify-send "Screenshot taken"
