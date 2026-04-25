#!/bin/bash


#current numbers of windows
cw=0

open(){
local win_name="$1"
local program="$2"
local wn=$3

$program &
sleep 0.5

while ! wmctrl -l | grep -i "$win_name" > /dev/null; do
	sleep 1
done

wmctrl -r $win_name -t $wn
wmctrl -r "$win_name" -b add,maximized_vert,maximized_horz
wmctrl -s $wn

}


wmctrl -n $cw
site1="https://poczta.agh.edu.pl/rcm-1.5/?_task=mail&_mbox=INBOX"
site2="https://www.messenger.com/t/25271575812455976"
site3="https://chatgpt.com/"
open "google chrome" "google-chrome --  $site1 $site2 $site3" $cw
cw=1
wmctrl -n $cw
wd="/home/serwyn/Python/WordDetectML/"
open "VSCodium" "codium $wd" $cw
cw=2
#TERMINAL_CUSTOM -> is a variable that accurs 2 time in this line -> be carefull with the chages


# commands='tmux new -t session_custom'
tmux_cmd='tmux split-window -h'
commands='tmux new -t build_session ||
tmux send-keys -t build_session $tmux_cmd C-m'

# open "Terminal_custom" "gnome-terminal --title=\"Terminal_custom\" -- bash -c \"$commands\"" $cw
open "Terminal" "gnome-terminal --title=\"Terminal\" -- bash -c $commands" $cw
wmctrl -s $cw

