let pc = null;
const videoStream = document.getElementById('videoStream');

async function VisionJoin() {
    const response = await fetch('/offer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify()
    })

    if(!response.ok){
        throw new Error('Failed to join session');
    }

    const data = await response.json();
    pc = new RTCPeerConnection();
    pc.ontrack = (event) => {
        videoStream.srcObject = event.stream[0];
        videoStream.autoplay = true;
    }

    const offer = new RTCSessionDescription(data);
    await pc.setRemoteDescription(offer);
    const answer = await pc.createAnswer();
    await pc.setLocalDescription(answer);

    await fetch('/answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({sdp: pc.localDescription.sdp, type: pc.localDescription.type})
    })
}