#!/bin/bash

picom --daemon &
# Generate new colors and set wallpaper with pywal
wal -i $(cat ~/.cache/wall) &
# Wait a moment for pywal to generate colors
sleep 1
# Launch polybar with new colors
~/.config/polybar/launch.sh &

# 1. Uncomment to restore last saved wallpaper
# xargs xwallpaper --stretch < ~/.cache/wall &
# 2. Uncomment to set a random wallpaper on login
# find ~/Pictures/Wallpapers -type f | shuf -n 1 | xargs xwallpaper --stretch &

