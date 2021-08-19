#!/bin/bash
MNT1="HDMI-0"
MNT2="DP-3"
BRT=0

echo "---> [-] Turning off the monitor..."
xrandr --output $MNT1 --brightness $BRT
xrandr --output $MNT2 --brightness $BRT
