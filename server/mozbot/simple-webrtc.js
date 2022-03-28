// ......................................................
// ..................RTCMultiConnection Code.............
// ......................................................


var roomid = window.location.hash.substr(1);

// just in case; normally this id comes from the pi connecting
if(roomid==""){
    roomid = parseInt(Math.random()*1000)+"";
}

var connection = new RTCMultiConnection();

// by default, socket.io server is assumed to be deployed on your own URL
connection.socketURL = '/';

// this is only useful if we want to do something server side
connection.socketMessageEvent = 'audio-data-video-asymmetric';

let streamz = [];

connection.onstream = function(event) {

  let the_id = event.stream.id
  console.log("streaming",event);

  if(event.type!="local"){
   console.log("REMOTE stream");
   try{

    if(streamz.includes(the_id)){
      console.log("already got id for local "+the_id);
    }else{
      const vid = document.querySelector('#remote');
      vid.srcObject = event.stream;
      streamz.push(the_id);
    }

   }catch(e){
     console.log("e - REMOTE",e);
   }
  }else{
    console.log("LOCAL stream");
    try{

      if(streamz.includes(the_id)){
        // there sometimes seem to be two
        console.log("already got id for remote "+the_id);
      }else{

        const vid = document.querySelector('#local');
        vid.srcObject = event.stream;

        if(i_am_remote){
 
          // a muted element is enough so we don't get talkback
          // but to really mute we also mute the stream itself
          // and remote only wants to start off muted

          window.local_stream = event.stream;
          window.local_stream.mute();

        }

        streamz.push(the_id);
      }

   }catch(e){
     console.log("e - LOCAL",e);
   }
  }
};


// https://www.rtcmulticonnection.org/docs/iceServers/
// use your own TURN-server here!
connection.iceServers = [{
  'urls': [
     'stun:stun.l.google.com:19302',
     'stun:stun1.l.google.com:19302',
     'stun:stun2.l.google.com:19302',
     'stun:stun.l.google.com:19302?transport=udp',

  ]
}];

createRoom = function() {
  console.log("creating room",roomid);
  connection.open(roomid, function() {
    showRoomURL(connection.sessionid);
  });
};

joinRoom = function() {
  console.log("joining room",roomid);
  connection.join(roomid, function() {
    showRoomURL(connection.sessionid);
  });
};

openOrJoinRoom = function() {
  console.log("joining room",roomid);
  connection.openOrJoin(roomid, function() {
     showRoomURL(connection.sessionid);
  });
};

connection.onstreamended = function(event) {
  var mediaElement = document.getElementById(event.streamid);
  if (mediaElement) {
    mediaElement.parentNode.removeChild(mediaElement);
  }
};

connection.onMediaError = function(e) {
  if (e.message === 'Concurrent mic process limit.') {
    if (DetectRTC.audioInputDevices.length <= 1) {
      alert('Please select external microphone. Check github issue number 483.');
      return;
    }

    var secondaryMic = DetectRTC.audioInputDevices[1].deviceId;
    connection.mediaConstraints.audio = {
      deviceId: secondaryMic
    };

    connection.join(connection.sessionid);
  }
};


function showRoomURL(roomid) {
  var roomHashURL = '#' + roomid;

  var html = 'room: <a href="' + roomHashURL + '" target="_blank">' + roomHashURL + '</a>';
  var roomURLsDiv = document.getElementById('room-urls');
  roomURLsDiv.innerHTML = html;

}

(function() {
  var params = {},
  r = /([^&=]+)=?([^&]*)/g;

  function d(s) {
    return decodeURIComponent(s.replace(/\+/g, ' '));
  }
   var match, search = window.location.search;
   while (match = r.exec(search.substring(1)))
   params[d(match[1])] = d(match[2]);
   window.params = params;
})();

