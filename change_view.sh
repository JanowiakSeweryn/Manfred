
if wmctrl -l | grep -i "$1"; then
	    wmctrl -a "$1"
    else
	        $2 &
fi
