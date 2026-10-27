// Metronome using Web Audio API with Lookahead Scheduling
// Eliminates timer drift for sample-accurate musical timing.

class Metronome {
    constructor(bpm = 120, beatsPerMeasure = 4) {
        this.bpm = parseInt(bpm, 10);
        this.beatsPerMeasure = parseInt(beatsPerMeasure, 10);
        this.isPlaying = false;
        this.audioCtx = null;
        this.currentBeat = 0;
        this.nextNoteTime = 0.0;
        this.timerId = null;
        this.lookahead = 25.0; // Lookahead interval in ms
        this.scheduleAheadTime = 0.1; // Scheduling horizon in seconds
        this.onBeat = null; // Callback for UI beat synchronization: (beatIndex, isAccent)
    }

    start() {
        if (this.isPlaying) return;

        // Initialize AudioContext on user gesture
        if (!this.audioCtx) {
            this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }

        if (this.audioCtx.state === 'suspended') {
            this.audioCtx.resume();
        }

        this.isPlaying = true;
        this.currentBeat = 0;
        this.nextNoteTime = this.audioCtx.currentTime + 0.05;

        // Run scheduler loop every 25ms
        this.timerId = setInterval(() => this.scheduler(), this.lookahead);
    }

    stop() {
        if (!this.isPlaying) return;
        this.isPlaying = false;
        clearInterval(this.timerId);
        this.timerId = null;
        this.currentBeat = 0;
    }

    scheduler() {
        // While there are notes that will need to play before next interval, schedule them
        while (this.nextNoteTime < this.audioCtx.currentTime + this.scheduleAheadTime) {
            this.scheduleNote(this.currentBeat, this.nextNoteTime);
            this.nextNote();
        }
    }

    nextNote() {
        const secondsPerBeat = 60.0 / this.bpm;
        this.nextNoteTime += secondsPerBeat;
        this.currentBeat = (this.currentBeat + 1) % this.beatsPerMeasure;
    }

    scheduleNote(beatNumber, time) {
        const isAccent = (beatNumber === 0);

        // Create oscillator & gain envelope
        const osc = this.audioCtx.createOscillator();
        const gain = this.audioCtx.createGain();

        // High pitch beep on beat 1 (accent), lower on other beats
        osc.type = 'sine';
        osc.frequency.setValueAtTime(isAccent ? 1200 : 800, time);

        // Quick punchy percussive click envelope
        gain.gain.setValueAtTime(1.0, time);
        gain.gain.exponentialRampToValueAtTime(0.001, time + 0.035);

        osc.connect(gain);
        gain.connect(this.audioCtx.destination);

        osc.start(time);
        osc.stop(time + 0.035);

        // Dispatch visual feedback timed with the sound
        const delayMs = Math.max(0, (time - this.audioCtx.currentTime) * 1000);
        setTimeout(() => {
            if (this.isPlaying && typeof this.onBeat === 'function') {
                this.onBeat(beatNumber, isAccent);
            }
        }, delayMs);
    }

    setBpm(newBpm) {
        const parsed = parseInt(newBpm, 10);
        if (!isNaN(parsed) && parsed >= 30 && parsed <= 300) {
            this.bpm = parsed;
        }
    }

    setBeatsPerMeasure(beats) {
        const parsed = parseInt(beats, 10);
        if (!isNaN(parsed) && parsed >= 1 && parsed <= 12) {
            this.beatsPerMeasure = parsed;
            this.currentBeat = 0;
        }
    }
}
