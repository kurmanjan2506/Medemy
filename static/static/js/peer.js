var mapPeers = {};

var mapScreenPeers = {};

var screenShared = false;

const localVideo = document.querySelector('#local-video');

var btnShareScreen = document.querySelector('#btn-share-screen');

var localStream = new MediaStream();

var localDisplayStream = new MediaStream();

btnToggleAudio = document.querySelector("#btn-toggle-audio");
btnToggleVideo = document.querySelector("#btn-toggle-video");

var messageInput = document.querySelector('#msg');
var btnSendMsg = document.querySelector('#btn-send-msg');

var btnRecordScreen = document.querySelector('#btn-record-screen');
var recorder;
var recording = false;

var file;

document.getElementById('share-file-button').addEventListener('click', () => {
    document.getElementById('select-file-dialog').style.display = 'block';
});

document.getElementById('cancel-button').addEventListener('click', () => {
    document.getElementById('select-file-input').value = '';
    document.getElementById('select-file-dialog').style.display = 'none';
    document.getElementById('ok-button').disabled = true;
});

document.getElementById('select-file-input').addEventListener('change', (event) => {
    file = event.target.files[0];
    document.getElementById('ok-button').disabled = !file;
});

var ul = document.querySelector("#message-list");

var loc = window.location;

var endPoint = '';
var wsStart = 'ws://';

if(loc.protocol == 'https:'){
    wsStart = 'wss://';
}

var endPoint = wsStart + loc.host + loc.pathname;

var webSocket;

var usernameInput = document.querySelector('#username');
var username;

var btnJoin = document.querySelector('#btn-join');

btnJoin.onclick = () => {
    username = usernameInput.value;

    if(username == ''){
        return;
    }

    usernameInput.value = '';
    btnJoin.disabled = true;
    usernameInput.style.visibility = 'hidden';
    btnJoin.disabled = true;
    btnJoin.style.visibility = 'hidden';

    document.querySelector('#label-username').innerHTML = username;

    webSocket = new WebSocket(endPoint);

    webSocket.onopen = function(e){
        console.log('Connection opened! ', e);

        sendSignal('new-peer', {
            'local_screen_sharing': false,
        });
    }

    webSocket.onmessage = webSocketOnMessage;

    webSocket.onclose = function(e){
        console.log('Connection closed! ', e);
    }

    webSocket.onerror = function(e){
        console.log('Error occured! ', e);
    }

    btnSendMsg.disabled = false;
    messageInput.disabled = false;
}

function webSocketOnMessage(event){
    var parsedData = JSON.parse(event.data);

    var action = parsedData['action'];
    var peerUsername = parsedData['peer'];

    console.log('peerUsername: ', peerUsername);
    console.log('action: ', action);

    if(peerUsername == username){
        return;
    }

    var remoteScreenSharing = parsedData['message']['local_screen_sharing'];
    console.log('remoteScreenSharing: ', remoteScreenSharing);

    var receiver_channel_name = parsedData['message']['receiver_channel_name'];
    console.log('receiver_channel_name: ', receiver_channel_name);

    if(action == 'new-peer'){
        console.log('New peer: ', peerUsername);

        createOfferer(peerUsername, false, remoteScreenSharing, receiver_channel_name);

        if(screenShared && !remoteScreenSharing){
            console.log('Creating screen sharing offer.');
            createOfferer(peerUsername, true, remoteScreenSharing, receiver_channel_name);
        }

        return;
    }

    var localScreenSharing = parsedData['message']['remote_screen_sharing'];

    if(action == 'new-offer'){
        console.log('Got new offer from ', peerUsername);

        var offer = parsedData['message']['sdp'];
        console.log('Offer: ', offer);
        var peer = createAnswerer(offer, peerUsername, localScreenSharing, remoteScreenSharing, receiver_channel_name);

        return;
    }


    if(action == 'new-answer'){
        var peer = null;

        if(remoteScreenSharing){
            peer = mapPeers[peerUsername + ' Screen'][0];
        }else if(localScreenSharing){
            peer = mapScreenPeers[peerUsername][0];
        }else{
            peer = mapPeers[peerUsername][0];
        }

        var answer = parsedData['message']['sdp'];

        console.log('mapPeers:');
        for(key in mapPeers){
            console.log(key, ': ', mapPeers[key]);
        }

        console.log('peer: ', peer);
        console.log('answer: ', answer);

        peer.setRemoteDescription(answer);

        return;
    }
}

messageInput.addEventListener('keyup', function(event){
    if(event.keyCode == 13){
        event.preventDefault();

        btnSendMsg.click();
    }
});

btnSendMsg.onclick = btnSendMsgOnClick;

function btnSendMsgOnClick(){
    var message = messageInput.value;

    var li = document.createElement("li");
    li.appendChild(document.createTextNode("Me: " + message));
    ul.appendChild(li);

    var dataChannels = getDataChannels();

    console.log('Sending: ', message);


    for(index in dataChannels){
        dataChannels[index].send(username + ': ' + message);
    }

    messageInput.value = '';
}

const constraints = {
    'video': true,
    'audio': true
}


userMedia = navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        localStream = stream;
        console.log('Got MediaStream:', stream);
        var mediaTracks = stream.getTracks();

        for(i=0; i < mediaTracks.length; i++){
            console.log(mediaTracks[i]);
        }

        localVideo.srcObject = localStream;
        localVideo.muted = true;

        window.stream = stream;

        audioTracks = stream.getAudioTracks();
        videoTracks = stream.getVideoTracks();

        audioTracks[0].enabled = true;
        videoTracks[0].enabled = true;

        btnToggleAudio.onclick = function(){
            audioTracks[0].enabled = !audioTracks[0].enabled;
            if(audioTracks[0].enabled){
                btnToggleAudio.innerHTML = 'Выключить микрофон';
                return;
            }

            btnToggleAudio.innerHTML = 'Включить микрофон';
        };

        btnToggleVideo.onclick = function(){
            videoTracks[0].enabled = !videoTracks[0].enabled;
            if(videoTracks[0].enabled){
                btnToggleVideo.innerHTML = 'Выключить камеру';
                return;
            }

            btnToggleVideo.innerHTML = 'Включить камеру';
        };
    })
    .then(e => {
        btnShareScreen.onclick = event => {
            if(screenShared){
                screenShared = !screenShared;

                localVideo.srcObject = localStream;
                btnShareScreen.innerHTML = 'Share screen';

                var localScreen = document.querySelector('#my-screen-video');
                removeVideo(localScreen);
                var screenPeers = getPeers(mapScreenPeers);
                for(index in screenPeers){
                    screenPeers[index].close();
                }
                mapScreenPeers = {};

                return;
            }

            screenShared = !screenShared;

            navigator.mediaDevices.getDisplayMedia(constraints)
                .then(stream => {
                    localDisplayStream = stream;

                    var mediaTracks = stream.getTracks();
                    for(i=0; i < mediaTracks.length; i++){
                        console.log(mediaTracks[i]);
                    }

                    var localScreen = createVideo('my-screen');
                    localScreen.srcObject = localDisplayStream;

                    sendSignal('new-peer', {
                        'local_screen_sharing': true,
                    });
                })
                .catch(error => {
                    console.log('Error accessing display media.', error);
                });

            btnShareScreen.innerHTML = 'Stop sharing';
        }
    })
    .then(e => {
        btnRecordScreen.addEventListener('click', () => {
            if(recording){
                // toggle recording
                recording = !recording;

                btnRecordScreen.innerHTML = 'Record Screen';

                recorder.stopRecording(function() {
                    var blob = recorder.getBlob();
                    invokeSaveAsDialog(blob);
                });

                return;
            }

            recording = !recording;

            navigator.mediaDevices.getDisplayMedia(constraints)
                .then(stream => {
                    recorder = RecordRTC(stream, {
                        type: 'video',
                        MimeType: 'video/mp4'
                    });
                    recorder.startRecording();

                    var mediaTracks = stream.getTracks();
                    for(i=0; i < mediaTracks.length; i++){
                        console.log(mediaTracks[i]);
                    }

                })
                .catch(error => {
                    console.log('Error accessing display media.', error);
                });

            btnRecordScreen.innerHTML = 'Stop Recording';
        });
    })
    .catch(error => {
        console.error('Error accessing media devices.', error);
    });

function sendSignal(action, message){
    webSocket.send(
        JSON.stringify(
            {
                'peer': username,
                'action': action,
                'message': message,
            }
        )
    )
}

function createOfferer(peerUsername, localScreenSharing, remoteScreenSharing, receiver_channel_name){
    var peer = new RTCPeerConnection(null);

    addLocalTracks(peer, localScreenSharing);

    var dc = peer.createDataChannel("channel");
    dc.onopen = () => {
        console.log("Connection opened.");
    };
    var remoteVideo = null;
    if(!localScreenSharing && !remoteScreenSharing){

        dc.onmessage = dcOnMessage;

        remoteVideo = createVideo(peerUsername);
        setOnTrack(peer, remoteVideo);
        console.log('Remote video source: ', remoteVideo.srcObject);

        mapPeers[peerUsername] = [peer, dc];

        peer.oniceconnectionstatechange = () => {
            var iceConnectionState = peer.iceConnectionState;
            if (iceConnectionState === "failed" || iceConnectionState === "disconnected" || iceConnectionState === "closed"){
                console.log('Deleting peer');
                delete mapPeers[peerUsername];
                if(iceConnectionState != 'closed'){
                    peer.close();
                }
                removeVideo(remoteVideo);
            }
        };
    }else if(!localScreenSharing && remoteScreenSharing){
        dc.onmessage = (e) => {
            console.log('New message from %s\'s screen: ', peerUsername, e.data);
        };

        remoteVideo = createVideo(peerUsername + '-screen');
        setOnTrack(peer, remoteVideo);
        console.log('Remote video source: ', remoteVideo.srcObject);

        mapPeers[peerUsername + ' Screen'] = [peer, dc];

        peer.oniceconnectionstatechange = () => {
            var iceConnectionState = peer.iceConnectionState;
            if (iceConnectionState === "failed" || iceConnectionState === "disconnected" || iceConnectionState === "closed"){
                delete mapPeers[peerUsername + ' Screen'];
                if(iceConnectionState != 'closed'){
                    peer.close();
                }
                removeVideo(remoteVideo);
            }
        };
    }else{

        dc.onmessage = (e) => {
            console.log('New message from %s: ', peerUsername, e.data);
        };

        mapScreenPeers[peerUsername] = [peer, dc];

        peer.oniceconnectionstatechange = () => {
            var iceConnectionState = peer.iceConnectionState;
            if (iceConnectionState === "failed" || iceConnectionState === "disconnected" || iceConnectionState === "closed"){
                delete mapScreenPeers[peerUsername];
                if(iceConnectionState != 'closed'){
                    peer.close();
                }
            }
        };
    }

    peer.onicecandidate = (event) => {
        if(event.candidate){
            console.log("New Ice Candidate! Reprinting SDP" + JSON.stringify(peer.localDescription));
            return;
        }


        console.log('Gathering finished! Sending offer SDP to ', peerUsername, '.');
        console.log('receiverChannelName: ', receiver_channel_name);

        sendSignal('new-offer', {
            'sdp': peer.localDescription,
            'receiver_channel_name': receiver_channel_name,
            'local_screen_sharing': localScreenSharing,
            'remote_screen_sharing': remoteScreenSharing,
        });
    }

    peer.createOffer()
        .then(o => peer.setLocalDescription(o))
        .then(function(event){
            console.log("Local Description Set successfully.");
        });

    console.log('mapPeers[', peerUsername, ']: ', mapPeers[peerUsername]);

    return peer;
}

function createAnswerer(offer, peerUsername, localScreenSharing, remoteScreenSharing, receiver_channel_name){
    var peer = new RTCPeerConnection(null);

    addLocalTracks(peer, localScreenSharing);

    if(!localScreenSharing && !remoteScreenSharing){
        var remoteVideo = createVideo(peerUsername);

        setOnTrack(peer, remoteVideo);

        peer.ondatachannel = e => {
            console.log('e.channel.label: ', e.channel.label);
            peer.dc = e.channel;
            peer.dc.onmessage = dcOnMessage;
            peer.dc.onopen = () => {
                console.log("Connection opened.");
            }

            mapPeers[peerUsername] = [peer, peer.dc];
        }

        peer.oniceconnectionstatechange = () => {
            var iceConnectionState = peer.iceConnectionState;
            if (iceConnectionState === "failed" || iceConnectionState === "disconnected" || iceConnectionState === "closed"){
                delete mapPeers[peerUsername];
                if(iceConnectionState != 'closed'){
                    peer.close();
                }
                removeVideo(remoteVideo);
            }
        };
    }else if(localScreenSharing && !remoteScreenSharing){

        peer.ondatachannel = e => {
            peer.dc = e.channel;
            peer.dc.onmessage = (evt) => {
                console.log('New message from %s: ', peerUsername, evt.data);
            }
            peer.dc.onopen = () => {
                console.log("Connection opened.");
            }

            mapScreenPeers[peerUsername] = [peer, peer.dc];

            peer.oniceconnectionstatechange = () => {
                var iceConnectionState = peer.iceConnectionState;
                if (iceConnectionState === "failed" || iceConnectionState === "disconnected" || iceConnectionState === "closed"){
                    delete mapScreenPeers[peerUsername];
                    if(iceConnectionState != 'closed'){
                        peer.close();
                    }
                }
            };
        }
    }else{
        var remoteVideo = createVideo(peerUsername + '-screen');
        setOnTrack(peer, remoteVideo);

        peer.ondatachannel = e => {
            peer.dc = e.channel;
            peer.dc.onmessage = evt => {
                console.log('New message from %s\'s screen: ', peerUsername, evt.data);
            }
            peer.dc.onopen = () => {
                console.log("Connection opened.");
            }

            mapPeers[peerUsername + ' Screen'] = [peer, peer.dc];

        }
        peer.oniceconnectionstatechange = () => {
            var iceConnectionState = peer.iceConnectionState;
            if (iceConnectionState === "failed" || iceConnectionState === "disconnected" || iceConnectionState === "closed"){
                delete mapPeers[peerUsername + ' Screen'];
                if(iceConnectionState != 'closed'){
                    peer.close();
                }
                removeVideo(remoteVideo);
            }
        };
    }

    peer.onicecandidate = (event) => {
        if(event.candidate){
            console.log("New Ice Candidate! Reprinting SDP" + JSON.stringify(peer.localDescription));
            return;
        }

        // event.candidate == null indicates that gathering is complete

        console.log('Gathering finished! Sending answer SDP to ', peerUsername, '.');
        console.log('receiverChannelName: ', receiver_channel_name);

        sendSignal('new-answer', {
            'sdp': peer.localDescription,
            'receiver_channel_name': receiver_channel_name,
            'local_screen_sharing': localScreenSharing,
            'remote_screen_sharing': remoteScreenSharing,
        });
    }

    peer.setRemoteDescription(offer)
        .then(() => {
            console.log('Set offer from %s.', peerUsername);
            return peer.createAnswer();
        })
        .then(a => {
            console.log('Setting local answer for %s.', peerUsername);
            return peer.setLocalDescription(a);
        })
        .then(() => {
            console.log('Answer created for %s.', peerUsername);
            console.log('localDescription: ', peer.localDescription);
            console.log('remoteDescription: ', peer.remoteDescription);
        })
        .catch(error => {
            console.log('Error creating answer for %s.', peerUsername);
            console.log(error);
        });

    return peer
}

function dcOnMessage(event){
    var message = event.data;

    var li = document.createElement("li");
    li.appendChild(document.createTextNode(message));
    ul.appendChild(li);
}

function getDataChannels(){
    var dataChannels = [];

    for(peerUsername in mapPeers){
        console.log('mapPeers[', peerUsername, ']: ', mapPeers[peerUsername]);
        var dataChannel = mapPeers[peerUsername][1];
        console.log('dataChannel: ', dataChannel);

        dataChannels.push(dataChannel);
    }

    return dataChannels;
}

function getPeers(peerStorageObj){
    var peers = [];

    for(peerUsername in peerStorageObj){
        var peer = peerStorageObj[peerUsername][0];
        console.log('peer: ', peer);

        peers.push(peer);
    }

    return peers;
}

function createVideo(peerUsername){
    var videoContainer = document.querySelector('#video-container');
    var remoteVideo = document.createElement('video');

    remoteVideo.id = peerUsername + '-video';
    remoteVideo.autoplay = true;
    remoteVideo.playsinline = true;
    var videoWrapper = document.createElement('div');

    videoContainer.appendChild(videoWrapper);

    videoWrapper.appendChild(remoteVideo);

    return remoteVideo;
}

function setOnTrack(peer, remoteVideo){
    console.log('Setting ontrack:');
    var remoteStream = new MediaStream();

    remoteVideo.srcObject = remoteStream;

    console.log('remoteVideo: ', remoteVideo.id);

    peer.addEventListener('track', async (event) => {
        console.log('Adding track: ', event.track);
        remoteStream.addTrack(event.track, remoteStream);
    });
}

function addLocalTracks(peer, localScreenSharing){
    if(!localScreenSharing){
        localStream.getTracks().forEach(track => {
            console.log('Adding localStream tracks.');
            peer.addTrack(track, localStream);
        });

        return;
    }

    localDisplayStream.getTracks().forEach(track => {
        console.log('Adding localDisplayStream tracks.');
        peer.addTrack(track, localDisplayStream);
    });
}

function removeVideo(video){
    var videoWrapper = video.parentNode;
    videoWrapper.parentNode.removeChild(videoWrapper);
}