
dbus-monitor "interface='org.freedesktop.Notifications'" | while read -r line; do
	
	let "counter++"
	if [[ "$line" == *"www.facebook.com"* ]]; then
		sendmsg= true
		# echo "LINE=facebook"
		continue
	fi
	
	# if [[ "$line" == *"array ["* ]]; then
	# 	sendmsg=false
	# 	echo "mesg closed"
	# fi
	if [ "$sendmsg" = true ]; then
		message="$line"
		message=${message//\"/}
		echo $message
		sendmsg=false
	fi

done

