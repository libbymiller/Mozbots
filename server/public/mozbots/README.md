# Mozbots

A peer.js pair where

 * remote is audio only, bot is video and audio
 * remote starts muted
 * remote does ot send video
 * id of bot comes from the hash part of the url
 * elements are removed on closing the call
 * various commands are possible via the data channel to the bot
 * remote video is fullscreen or near

index.html shows recently seen bots.
I've made a one-line edit to peerjs.js at line 7972:

   _this.connection.emit(enums_1.PeerEventType.Disconnected, peerId);

There are some legacy configs in there I used for a respeaker and amp setup, but this doesn't work well; we now recommend using a Sennheiser 20.

# stun / turn:

    sudo apt-get -y install coturn

    sudo nano /etc/turnserver.conf

contents

    realm=coturn.myserver.example.com
    fingerprint
    listening-ip=0.0.0.0
    external-ip=<EXTERNAL_IP>/<INTERNAL_IP> #or just the external ip
    listening-port=3478
    min-port=10000
    max-port=20000
    log-file=/var/log/turnserver.log
    verbose
    user=something:something
    lt-cred-mech


sudo nano /etc/default/coturn

    TURNSERVER_ENABLED=1


OPEN PORT tcp:3478 (and udp?)

check:

    netstat -pnltu | grep 3478

and setup for peer.js is

    var peer = new Peer(
    {
      key: 'peerjs', host: 'myserver.example.com', path: "/",debug:3, port: 443, secure: true,
      config: {'iceServers': [
       { url: 'turn:myserver.example.com:3478?transport=udp', username: 'something', credential: 'something' },
       { url: 'turn:myserver.example.com:3478?transport=tcp', username: 'something', credential: 'something' }
      ]}
    });
