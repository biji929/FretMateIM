// Tuner (basic structure)
async function initTuner() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const audioCtx = new AudioContext();
        const analyser = audioCtx.createAnalyser();
        const source = audioCtx.createMediaStreamSource(stream);
        source.connect(analyser);
        // ... pitch detection logic using autocorrelation
    } catch (err) {
        alert('Tuner requires microphone access.');
    }
}
