// Metronome using Web Audio API
class Metronome {
    constructor(bpm = 120) {
        this.bpm = bpm;
        this.isPlaying = false;
        this.audioCtx = null;
        this.timerID = null;
    }

    start() {
        if (this.isPlaying) return;
        this.isPlaying = true;
        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        // Basic interval implementation for demo
        this.timerID = setInterval(() => this.playClick(), (60 / this.bpm) * 1000);
    }

    stop() {
        this.isPlaying = false;
        clearInterval(this.timerID);
        if (this.audioCtx) {
            this.audioCtx.close();
        }
    }

    playClick() {
        if (!this.audioCtx) return;
        const osc = this.audioCtx.createOscillator();
        const gain = this.audioCtx.createGain();
        osc.frequency.setValueAtTime(1000, this.audioCtx.currentTime);
        gain.gain.setValueAtTime(1, this.audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + 0.05);
        osc.connect(gain);
        gain.connect(this.audioCtx.destination);
        osc.start();
        osc.stop(this.audioCtx.currentTime + 0.05);
    }
}
