#! /bin/sh
maim --select --hidecursor /home/slats/Images/Screenshots/$(date +%Y-%b-%d--%H-%M-%S_maim | tr A-Z a-z).png
notify-send "Screenshot taken"
