#! /bin/sh
maim --window $(xdotool getactivewindow) /mnt/data/Images/Screenshots/$(date +%Y-%b-%d--%H-%M-%S_maim | tr A-Z a-z).png
notify-send "Screenshot taken"
mpv --no-video /home/slats/.config/qtile/resources/foto.wav
