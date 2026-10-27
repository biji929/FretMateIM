// Guitar Tuner for FretMate
// Uses Web Audio API + Time-Domain Autocorrelation for accurate real-time pitch detection.

const NOTE_STRINGS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

// Standard 6-string guitar tunings (EADGBE)
const STANDARD_GUITAR_NOTES = [
    { name: 'E2', stringNum: 6, freq: 82.41, midiNote: 40 },
    { name: 'A2', stringNum: 5, freq: 110.00, midiNote: 45 },
    { name: 'D3', stringNum: 4, freq: 146.83, midiNote: 50 },
    { name: 'G3', stringNum: 3, freq: 196.00, midiNote: 55 },
    { name: 'B3', stringNum: 2, freq: 246.94, midiNote: 59 },
    { name: 'E4', stringNum: 1, freq: 329.63, midiNote: 64 },
];

class GuitarTuner {
    constructor() {
        this.audioCtx = null;
        this.analyser = null;
        this.mediaStream = null;
        this.isListening = false;
        this.animationFrameId = null;
        this.buffer = null;
        this.onNoteDetected = null; // Callback: (noteData)
        this.onSilent = null;       // Callback when input is below noise threshold
    }

    async start() {
        if (this.isListening) return;

        // Request clean microphone audio stream
        try {
            this.mediaStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: false,
                    autoGainControl: false,
                    noiseSuppression: false,
                }
            });
        } catch (e) {
            // Fallback for browsers that enforce standard constraints
            this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        }

        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (this.audioCtx.state === 'suspended') {
            await this.audioCtx.resume();
        }

        this.analyser = this.audioCtx.createAnalyser();
        this.analyser.fftSize = 2048;
        this.buffer = new Float32Array(this.analyser.fftSize);

        const source = this.audioCtx.createMediaStreamSource(this.mediaStream);
        source.connect(this.analyser);

        this.isListening = true;
        this.updateLoop();
    }

    stop() {
        if (!this.isListening) return;
        this.isListening = false;

        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }

        if (this.mediaStream) {
            this.mediaStream.getTracks().forEach(track => track.stop());
            this.mediaStream = null;
        }

        if (this.audioCtx) {
            this.audioCtx.close();
            this.audioCtx = null;
        }
    }

    updateLoop() {
        if (!this.isListening) return;

        this.analyser.getFloatTimeDomainData(this.buffer);
        const pitch = this.autoCorrelate(this.buffer, this.audioCtx.sampleRate);

        if (pitch === -1) {
            if (typeof this.onSilent === 'function') {
                this.onSilent();
            }
        } else {
            const noteData = this.getNoteDetails(pitch);
            if (typeof this.onNoteDetected === 'function') {
                this.onNoteDetected(noteData);
            }
        }

        this.animationFrameId = requestAnimationFrame(() => this.updateLoop());
    }

    // High precision autocorrelation pitch detector
    autoCorrelate(buffer, sampleRate) {
        const SIZE = buffer.length;
        let sumSquares = 0;
        for (let i = 0; i < SIZE; i++) {
            const val = buffer[i];
            sumSquares += val * val;
        }
        const rms = Math.sqrt(sumSquares / SIZE);

        // Signal is below threshold (ambient noise/silence)
        if (rms < 0.015) {
            return -1;
        }

        // Trim boundaries where signal is close to zero
        let r1 = 0;
        let r2 = SIZE - 1;
        const thres = 0.2;
        for (let i = 0; i < SIZE / 2; i++) {
            if (Math.abs(buffer[i]) < thres) {
                r1 = i;
                break;
            }
        }
        for (let i = 1; i < SIZE / 2; i++) {
            if (Math.abs(buffer[SIZE - i]) < thres) {
                r2 = SIZE - i;
                break;
            }
        }

        const trimmed = buffer.slice(r1, r2);
        const c = new Float32Array(trimmed.length).fill(0);

        for (let i = 0; i < trimmed.length; i++) {
            for (let j = 0; j < trimmed.length - i; j++) {
                c[i] = c[i] + trimmed[j] * trimmed[j + i];
            }
        }

        // Find the first dip
        let d = 0;
        while (d < trimmed.length - 1 && c[d] > c[d + 1]) {
            d++;
        }

        // Find peak after dip
        let maxval = -1;
        let maxpos = -1;
        for (let i = d; i < trimmed.length; i++) {
            if (c[i] > maxval) {
                maxval = c[i];
                maxpos = i;
            }
        }

        let T0 = maxpos;
        if (T0 <= 0 || T0 >= trimmed.length - 1) return -1;

        // Parabolic interpolation for fine sub-sample estimation
        const x1 = c[T0 - 1];
        const x2 = c[T0];
        const x3 = c[T0 + 1];
        const a = (x1 + x3 - 2 * x2) / 2;
        const b = (x3 - x1) / 2;
        if (a) {
            T0 = T0 - b / (2 * a);
        }

        const frequency = sampleRate / T0;

        // Plausible guitar range: 60 Hz (low dropped tunings) to 1200 Hz
        if (frequency < 60 || frequency > 1200) {
            return -1;
        }

        return frequency;
    }

    getNoteDetails(frequency) {
        // Calculate MIDI note: A4 = 440 Hz = MIDI note 69
        const noteNum = 12 * (Math.log(frequency / 440) / Math.log(2)) + 69;
        const roundedNote = Math.round(noteNum);
        const noteName = NOTE_STRINGS[roundedNote % 12];
        const octave = Math.floor(roundedNote / 12) - 1;

        // Target frequency for this note
        const targetFreq = 440 * Math.pow(2, (roundedNote - 69) / 12);

        // Deviation in cents (-50 to +50)
        const cents = Math.floor(1200 * (Math.log(frequency / targetFreq) / Math.log(2)));

        // Match against standard 6-string guitar
        const matchingString = STANDARD_GUITAR_NOTES.find(str => str.midiNote === roundedNote) || null;

        return {
            frequency: frequency,
            targetFreq: targetFreq,
            note: noteName,
            octave: octave,
            fullName: `${noteName}${octave}`,
            cents: cents,
            matchingString: matchingString,
            inTune: Math.abs(cents) <= 4
        };
    }
}
