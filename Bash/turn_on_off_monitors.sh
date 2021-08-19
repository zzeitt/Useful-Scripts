#!/bin/bash
BRT=`xrandr --verbose | grep -m 1 -i brightness | cut -f2 -d ' '`
MNT1="HDMI-0"
MNT2="DP-3"

echo "$MNT1's brightness is $BRT"

if [[ $BRT = "1.0" ]]
then
    echo "---> [-] Turning off the monitor..."
    xrandr --output $MNT1 --brightness 0
else
    echo "---> [O] Turn on the monitor."
    xrandr --output $MNT1 --brightness 1
fi

echo "$MNT2's brightness is $BRT"
if [[ $BRT = "1.0" ]]
then
    echo "---> [-] Turning off the monitor..."
    xrandr --output $MNT2 --brightness 0
else
    echo "---> [O] Turn on the monitor."
    xrandr --output $MNT2 --brightness 1
fi