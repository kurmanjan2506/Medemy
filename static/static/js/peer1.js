var loc = window.location;

var endPoint = '';
var wsStart = 'ws://';

console.log('protocol: ', loc.protocol);
if(loc.protocol == 'https:'){
    wsStart = 'wss://';
}

var endPoint = wsStart + loc.host + loc.pathname;

var webSocket = new WebSocket(endPoint);

webSocket.onopen = function(e){
    console.log('Connection opened! ', e);
}

webSocket.onmessage = webSocketOnMessage;

webSocket.onclose = function(e){
    console.log('Connection closed! ', e);

    peer1.close();
}

webSocket.onerror = function(e){
    console.log('Error occured! ', e);
}

var btnSendOffer = document.querySelector('#btn-send-offer');

btnSendOffer.onclick = btnSendOfferOnClick;

function webSocketOnMessage(event){
    var parsed_data = JSON.parse(event.data);

    var action = parsed_data['action'];

    if(parsed_data['peer'] == 'peer1'){
        return;
    }else if(action == 'peer2-candidate'){
        peer1.addIceCandidate(parsed_data['message']);
        return;
    }

    const thisPeer = parsed_data['peer'];
    const answer = parsed_data['message'];
    console.log('thisPeer: ', thisPeer);
    console.log('Answer received: ', answer);

    peer1.setRemoteDescription(answer);
}

btnPlayRemoteVideo = document.querySelector('#btn-play-remote-video');
btnPlayRemoteVideo.addEventListener("click", function (){
    remoteVideo.play();
    btnPlayRemoteVideo.style.visibility = 'hidden';
});

function sendSignal(thisPeer, action, message){
    webSocket.send(
        JSON.stringify(
            {
                'peer': thisPeer,
                'action': action,
                'message': message,
            }
        )
    )
}

function btnSendOfferOnClick(event){
    sendSignal('peer1', 'send-offer', peer1.localDescription);

    btnSendOffer.style.visibility = 'hidden';
}

var btnSendMsg = document.querySelector('#btn-send-msg');
btnSendMsg.onclick = btnSendMsgOnClick;

function btnSendMsgOnClick(){
    var messageInput = document.querySelector('#msg');
    var message = messageInput.value;

    var li = document.createElement("li");
    li.appendChild(document.createTextNode("Me: " + message));
    ul.appendChild(li);

    console.log('Sending: ', message);

    dc.send(message);

    messageInput.value = '';
}

const constraints = {
    'video': true,
    'audio': true
}

const iceConfiguration = {
    iceServers: [
        {
            urls: ['turn:numb.viagenie.ca'],
            credential: '{{numb_turn_credential}}',
            username: '{{numb_turn_username}}'
        }
    ]
};


var peer1;

var dc;

var screenShared = false;

const localVideo = document.querySelector('#local-video');
var remoteVideo;

var btnPlayRemoteVideo;

var btnShareScreen = document.querySelector('#btn-share-screen');

var localStream = new MediaStream();

var remoteStream;

var localDisplayStream = new MediaStream();

var ul = document.querySelector("#message-list");

userMedia = navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        localStream = stream;
        console.log('Got MediaStream:', stream);
        mediaTracks = stream.getTracks();

        for(i=0; i < mediaTracks.length; i++){
            console.log(mediaTracks[i]);
        }

        localVideo.srcObject = localStream;
        localVideo.muted = true;

        window.stream = stream;
    })
    .then(e => {
        btnShareScreen.onclick = event => {
            if(screenShared){
                screenShared = !screenShared;


                localVideo.srcObject = localStream;
                btnShareScreen.innerHTML = 'Share screen';

                return;
            }

            screenShared = !screenShared;

            navigator.mediaDevices.getDisplayMedia(constraints)
                .then(stream => {
                    localDisplayStream = stream;

                    localVideo.srcObject = localDisplayStream;
                });

            btnShareScreen.innerHTML = 'Stop sharing';
        }
    })
    .then(e => {
        createOfferer();
    })
    .catch(error => {
        console.error('Error accessing media devices.', error);
    });

function createOfferer(){
    peer1 = new RTCPeerConnection(null);

    localStream.getTracks().forEach(track => {
        peer1.addTrack(track, localStream);
    });

    localDisplayStream.getTracks().forEach(track => {
        peer1.addTrack(track, localDisplayStream);
    });

    dc = peer1.createDataChannel("channel");
    dc.onmessage = dcOnMessage
    dc.onopen = () => {
        console.log("Connection opened.");

        btnPlayRemoteVideo.style.visibility = 'visible';
    }

    peer1.onicecandidate = (event) => {
        if(event.candidate){
            console.log("New Ice Candidate! Reprinting SDP" + JSON.stringify(peer1.localDescription));
        }else{
            console.log('Gathering finished!');

        }
    }

    remoteStream = new MediaStream();
    remoteVideo = document.querySelector('#remote-video');
    remoteVideo.srcObject = remoteStream;

    peer1.addEventListener('track', async (event) => {
        remoteStream.addTrack(event.track, remoteStream);
    });

    peer1.createOffer()
        .then(o => peer1.setLocalDescription(o))
        .then(function(event){
            console.log("Local Description Set successfully.");
        });

    function dcOnMessage(event){
        var message = event.data;

        var li = document.createElement("li");
        li.appendChild(document.createTextNode("Other: " + message));
        ul.appendChild(li);
    }
}