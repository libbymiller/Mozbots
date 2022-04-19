# peer-js-simple-av-example

WIP -

 * peer js server + express
 * with apache ssl config

# Apache SSL config

Follow letsencrypt to get a generated ssl apache config file

```
sudo a2ensite example.conf
sudo a2enmod rewrite proxy proxy_balancer proxy_wstunnel proxy_http
sudo service apache2 reload
sudo service apache2 restart
```

# Add certs

```
sudo apt install certbot
sudo apt install python3-certbot-apache
```

# get the cert  

`sudo certbot --apache -d myserver.example.com --post-hook "/usr/sbin/service apache2 restart"`

then edit to match example in this dir: example-le-ssl.conf and restart apache.

idea is to proxy ssl to 8443 node server below, including wss

# setup peer.js server with express

as per: https://github.com/peers/peerjs-server

check out this repo

```
npm install peer
sudo node server.js
```

(sudo becuase of access to the ssl certs)

and go to https://myserver.example.com/test.html

# Paired bot and remote.html

peer.js requires one party to make the call and for that it needs to know the other one's peerid. In this example it uses the text after the # in the url. You can test with two windows open one with bot.html one with remote.html.

For the data examples you need to connect before sending a message. Only remote.html can initiate a call.

# Weirdnesses

I only really found 2, both with asymmetric - video one way and audio the other

 * unless you put constraints in, you get only audio both ways (https://github.com/peers/peerjs/issues/147#issuecomment-647498880)
 * The video is duplicated for remote

# multiplayer

It appears that peerjs can do more than 2 peers, but not tested this fully.
