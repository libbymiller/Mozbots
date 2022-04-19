#!/bin/bash

myrandom=$RANDOM
echo $myrandom

# kill any remaining bits
pkill -o chromium
sudo pkill -o websocketServer.py


# sometimes useful to kill the whole profile
#rm -rf /home/pi/.config/chromium/

# this is for bad crashes, which leave a lock handing round
rm /home/pi/.config/chromium/SingletonLock

# run the server
sudo python3 /home/pi/websocketServer.py &

# run the browser
# you can have a random room number

/usr/bin/chromium-browser --headless --disable-gpu --use-fake-ui-for-media-stream --autoplay-policy=no-user-gesture-required --allow-running-insecure-content --remote-debugging-port=9996 --remote-debugging-address=0.0.0.0 https://myserver.example.com/mozbot/bot.html#mozbot

