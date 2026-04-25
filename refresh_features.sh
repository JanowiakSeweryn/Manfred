#!/bin/bash

echo "-- initializing new features --"

# the & sign makes the procces in the background
python3 convert_data.py &

PID=$! #last background procces 

while kill -0 $PID 2>/dev/null; do
	for dots in "." ".." "..." "...."; do
		echo -ne "\rconverting the data$dots"
		sleep 0.5
	done
done

echo "data converted succesfully!"
echo " -- initialized traing model --"
 
python3 train.py upgrade_model & 

PID=$! #last background procces 

while kill -0 $PID 2>/dev/null; do
	for dots in "." ".." "..." "...."; do
		echo -ne "\rtraining the  data$dots"
		sleep 0.5
	done
done



if [ $! -eq "test" ]; then
	python3 "$1.py"
fi
