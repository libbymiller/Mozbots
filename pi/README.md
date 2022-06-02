# INSTALL

You need a server first.

# 0. assemble things

 * pi zero 2 w + 8 gb card, usb speakermic (or amp and respeaker 4 usb), pi camera, 2 servos
 * see [BOM](mozbots_bom.csv)
 * and [Fritzing diagram](mozbots_fritzing.png)

# 1. burn a card

I used buster (legacy) lite

# 2. enable ssh and wifi

    touch /Volumes/boot/ssh
    nano /Volumes/boot/wpa_supplicant.conf


contents

    country=GB
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
       ssid="xxx"
       psk="xxx"
    }

eject card and put in the pi

# 3. login

change device hostname

    pi@raspberrypi:~ $ sudo nano /etc/hosts
    pi@raspberrypi:~ $ sudo nano /etc/hostname

    sudo raspi-config

enable camera

reboot


# 4. test chromium stuff

    sudo apt-get update
    sudo apt-get install chromium-browser
    sudo apt-get install pulseaudio

note that 92 is broken - https://forums.raspberrypi.com/viewtopic.php?p=1919570&sid=175fb469cd6e74b67f364d46765b827c#p1919570

(it's still useful to install 92 to get the dependencies)

if you end up with 92, try

    wget  "http://archive.raspberrypi.org/debian/pool/main/c/chromium-browser/chromium-browser_88.0.4324.187-rpt1_armhf.deb"
    wget "http://archive.raspberrypi.org/debian/pool/main/c/chromium-browser/chromium-codecs-ffmpeg-extra_88.0.4324.187-rpt1_armhf.deb"
    sudo apt install --no-install-recommends --allow-downgrades --allow-change-held-packages ./chromium-browser_88.0.4324.187-rpt1_armhf.deb ./chromium-codecs-ffmpeg-extra_88.0.4324.187-rpt1_armhf.deb

    chromium-browser --version

-> 88


# 4. Attach camera and usb audio card, enable usb audio

    sudo nano /boot/config.txt 

    #dtparam=audio=on ## comment this out and save the file

    sudo nano /lib/modprobe.d/aliases.conf

    #options snd-usb-audio index=-2 # comment this out and save

and! (on a pi 4)

    sudo raspi-config

-> advanced options -> HDMI / Composite -> Default

(actually need selecting - possible bug? https://forums.raspberrypi.com/viewtopic.php?t=263942#p1706540)

reboot then

check usb with 

    aplay -l
    arecord -l

check speakers with

    speaker-test

check browser with 

    chromium-browser --headless --disable-gpu --use-fake-ui-for-media-stream --autoplay-policy=no-user-gesture-required --remote-debugging-port=9996 --remote-debugging-address=0.0.0.0 --allow-running-insecure-content https://myserver.example.com/mozbot/bot.html#mozbot

# 5. add start script and make it executable

clone this repo in /home/pi

    sudo apt-get install git

    cd
    git clone https://github.com/libbymiller/Mozbots

    cp /home/pi/Mozbots/pi/start_all.sh .

    chmod a+x start_all.sh 


# 6. Add websocket server

    sudo apt-get install python3-pip
    sudo pip3 install SimpleWebSocketServer #sudo because we're going to run it as root

    cd
    cp /home/pi/Mozbots/pi/websocketServer.py .

# 7. run on boot

    sudo cp /home/pi/Mozbots/pi/mozbot.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable mozbot

reboot


# 8. test

(assuming you have installed a server (see server instructions) at myserver.example.com) - go to 

https://myserver.example.com/mozbots/remote.html#mozbot


# Neopixel notes

https://magpi.raspberrypi.com/articles/neopixels-python
curl https://raw.githubusercontent.com/themagpimag/monthofmaking2019/master/DisplayLights/rollcall.py

LED_COUNT   = 24      # Number of LED pixels.
LED_ORDER = neopixel.GRBW


    sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
    sudo pip3 install adafruit-blinka
    sudo apt install python3-numpy

----

todo

lower volume?


