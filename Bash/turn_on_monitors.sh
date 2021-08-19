#!/bin/bash
MNT1="HDMI-0"
MNT2="DP-3"
BRT=1

echo "---> [O] Turn on the monitor."
xrandr --output $MNT1 --brightness $BRT
xrandr --output $MNT2 --brightness $BRT
