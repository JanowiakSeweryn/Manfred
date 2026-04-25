#!/bin/bash

# Pipe the monitor directly into the while loop
dbus-monitor "interface='org.freedesktop.Notifications'" | while read -r line; do

    # 1. Detect the start (messenger.com)
    if [[ "$line" == *"www.messenger.com"* ]]; then
        inside=true
        # Extract everything after the URL on the same line (if any)
        # and remove the trailing quote
        msg=$(echo "$line" | sed 's/.*www\.messenger\.com//;s/"$//')
        
        # Only print if there's actual text left after messenger.com
        [[ -n "${msg// /}" ]] && echo "$msg"
        continue
    fi

    # 2. Detect the end (The 'array' keyword)
    # Since we aren't grepping for "string", we can see this line now!
    if [[ "$line" == *"array ["* ]]; then
        inside=false
    fi

    # 3. If we are currently "inside" the message block, clean and print
    if [ "$inside" = true ]; then
        # Check if the line actually contains a string value
        if [[ "$line" == *"string "* ]]; then
            # Strip 'string "' from start and '"' from end
            echo "$line" | sed 's/^[[:space:]]*string "//;s/"$//'
        fi
    fi
done
