#!/bin/bash
BRT=`xrandr --verbose | grep -m 1 -i brightness | cut -f2 -d ' '`
MNT="HDMI-0"
echo "$MNT's brightness is $BRT"

if [[ $BRT = "1.0" ]]
then
    echo "---> [-] Turning off the monitor..."
    xrandr --output $MNT --brightness 0
else
    echo "---> [O] Turn on the monitor."
    xrandr --output $MNT --brightness 1
fi