import fs from 'fs';
import path from 'path';

/**
 * MUSIC FACTORY - NetworkBuster Audio Engine
 * Demonstrates:
 * 1. Synthesize Sound (WAV generation)
 * 2. Generate MIDI (Raw byte construction)
 * 3. Web Audio API (UI component)
 * 4. Algorithmic Composition (Melody generation)
 */

const SAMPLE_RATE = 44100;

// 1. SYNTHESIZE SOUND (WAV Generation)
export function generateWav(frequency = 440, durationSeconds = 2, waveform = 'sine') {
    const numSamples = SAMPLE_RATE * durationSeconds;
    const buffer = Buffer.alloc(44 + numSamples * 2); // 44 byte header + 16-bit PCM

    // RIFF Header
    buffer.write('RIFF', 0);
    buffer.writeUInt32LE(36 + numSamples * 2, 4);
    buffer.write('WAVE', 8);
    buffer.write('fmt ', 12);
    buffer.writeUInt32LE(16, 16); // Subchunk1Size
    buffer.writeUInt16LE(1, 20);  // AudioFormat (PCM)
    buffer.writeUInt16LE(1, 22);  // NumChannels (Mono)
    buffer.writeUInt32LE(SAMPLE_RATE, 24); // SampleRate
    buffer.writeUInt32LE(SAMPLE_RATE * 2, 28); // ByteRate
    buffer.writeUInt16LE(2, 32);  // BlockAlign
    buffer.writeUInt16LE(16, 34); // BitsPerSample
    buffer.write('data', 36);
    buffer.writeUInt32LE(numSamples * 2, 40);

    // Generate PCM Data
    for (let i = 0; i < numSamples; i++) {
        let sample = 0;
        const t = i / SAMPLE_RATE;
        
        if (waveform === 'sine') {
            sample = Math.sin(2 * Math.PI * frequency * t);
        } else if (waveform === 'square') {
            sample = Math.sin(2 * Math.PI * frequency * t) >= 0 ? 1 : -1;
        } else if (waveform === 'sawtooth') {
            sample = 2 * (t * frequency - Math.floor(t * frequency + 0.5));
        } else if (waveform === 'triangle') {
            sample = Math.asin(Math.sin(2 * Math.PI * frequency * t)) / (Math.PI / 2);
        }

        const volume = 0.5;
        const intSample = Math.floor(sample * volume * 32767);
        buffer.writeInt16LE(intSample, 44 + i * 2);
    }

    const fileName = `synth-${waveform}-${frequency}hz.wav`;
    fs.writeFileSync(fileName, buffer);
    return fileName;
}

// 2. GENERATE MIDI (Raw Byte Construction)
// Simplified MIDI file generator for a single track
export function generateMidi(notes = [60, 62, 64, 65, 67, 69, 71, 72]) {
    const header = Buffer.from([
        0x4D, 0x54, 0x68, 0x64, // MThd
        0x00, 0x00, 0x00, 0x06, // Header size
        0x00, 0x00,             // Format 0
        0x00, 0x01,             // One track
        0x00, 0x80              // 128 ticks per quarter note
    ]);

    let trackData = [];
    const velocity = 0x64;
    const duration = 0x80; // Quarter note

    notes.forEach(note => {
        // Note On: Delta time 0, Status 0x90, Note, Velocity
        trackData.push(0x00, 0x90, note, velocity);
        // Note Off: Delta time 'duration', Status 0x80, Note, Velocity 0
        trackData.push(duration, 0x80, note, 0x00);
    });

    // End of Track event
    trackData.push(0x01, 0xFF, 0x2F, 0x00);

    const trackHeader = Buffer.alloc(8);
    trackHeader.write('MTrk', 0);
    trackHeader.writeUInt32BE(trackData.length, 4);

    const midiBuffer = Buffer.concat([header, trackHeader, Buffer.from(trackData)]);
    const fileName = 'melody.mid';
    fs.writeFileSync(fileName, midiBuffer);
    return fileName;
}

// 4. ALGORITHMIC COMPOSITION (C Major Scale Melody)
export function composeMelody(length = 16) {
    const cMajor = [60, 62, 64, 65, 67, 69, 71, 72];
    const melody = [];
    let lastNoteIndex = 0;

    for (let i = 0; i < length; i++) {
        // Random walk: move up or down the scale by max 2 steps
        const step = Math.floor(Math.random() * 5) - 2;
        lastNoteIndex = Math.max(0, Math.min(cMajor.length - 1, lastNoteIndex + step));
        melody.push(cMajor[lastNoteIndex]);
    }

    return melody;
}

// 3. WEB AUDIO API (Component for UI)
export const WebAudioUI = `
<div class="glass" style="margin-top:20px;">
    <div class="card-title">Algorithmic Composer</div>
    
    <div style="display: flex; gap: 5px; margin-bottom: 10px;">
        <button class="btn" style="flex:1; font-size: 0.6rem; padding: 5px;" onclick="setWave('sine')">SINE</button>
        <button class="btn" style="flex:1; font-size: 0.6rem; padding: 5px;" onclick="setWave('square')">SQUARE</button>
        <button class="btn" style="flex:1; font-size: 0.6rem; padding: 5px;" onclick="setWave('sawtooth')">SAW</button>
        <button class="btn" style="flex:1; font-size: 0.6rem; padding: 5px;" onclick="setWave('triangle')">TRI</button>
    </div>

    <div id="piano-roll" style="display:grid; grid-template-columns: repeat(16, 1fr); gap:2px; height:60px; margin-bottom:15px; background: rgba(0,0,0,0.3); border-radius: 4px; padding: 5px;">
        <!-- Notes will appear here -->
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <button class="btn" onclick="composeAndPlay()">GENERATE_&_PLAY</button>
        <button class="btn" style="border-color: #ff4b2b; color: #ff4b2b;" onclick="stopAll()">STOP_ALL</button>
    </div>

    <div style="display: flex; gap: 5px; margin-top: 10px;">
        <button class="btn" style="flex:1; font-size: 0.6rem; border-color: var(--neon-purple); color: var(--neon-purple);" onclick="setScale('major')">MAJOR</button>
        <button class="btn" style="flex:1; font-size: 0.6rem; border-color: var(--neon-purple); color: var(--neon-purple);" onclick="setScale('minor')">MINOR</button>
        <button class="btn" style="flex:1; font-size: 0.6rem; border-color: var(--neon-purple); color: var(--neon-purple);" onclick="setScale('pentatonic')">PENTA</button>
    </div>

    <div id="composition-log" class="status">OSCILLATOR_READY | SCALE: MAJOR | WAVE: TRI</div>
</div>
<script>
    let audioCtx = null;
    let activeNodes = [];
    let currentWave = 'triangle';
    let currentScale = 'major';

    const scales = {
        major: [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25],
        minor: [261.63, 293.66, 311.13, 349.23, 392.00, 415.30, 466.16, 523.25],
        pentatonic: [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25]
    };

    function initAudio() {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    function setWave(w) { 
        currentWave = w; 
        updateLog(); 
    }
    
    function setScale(s) { 
        currentScale = s; 
        updateLog(); 
    }

    function updateLog() {
        document.getElementById('composition-log').textContent = \`OSCILLATOR_READY | SCALE: \${currentScale.toUpperCase()} | WAVE: \${currentWave.toUpperCase()}\`;
    }

    function stopAll() {
        activeNodes.forEach(n => { try { n.stop(); } catch(e) {} });
        activeNodes = [];
        document.getElementById('composition-log').textContent = 'AUDIO_HALTED_SUCCESSFULLY';
    }
    
    function playNote(freq, start, duration) {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        
        osc.type = currentWave;
        osc.frequency.setValueAtTime(freq, start);
        
        gain.gain.setValueAtTime(0.2, start);
        gain.gain.exponentialRampToValueAtTime(0.001, start + duration);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start(start);
        osc.stop(start + duration);
        activeNodes.push(osc);
    }

    function composeAndPlay() {
        initAudio();
        stopAll();
        const notes = scales[currentScale];
        let now = audioCtx.currentTime;
        const pianoRoll = document.getElementById('piano-roll');
        pianoRoll.innerHTML = '';
        
        for(let i=0; i<16; i++) {
            const noteIndex = Math.floor(Math.random() * notes.length);
            const freq = notes[noteIndex];
            playNote(freq, now + (i * 0.25), 0.2);
            
            const block = document.createElement('div');
            block.style.background = currentWave === 'square' ? 'var(--neon-blue)' : 'var(--neon-purple)';
            block.style.height = (noteIndex + 1) * 10 + '%';
            block.style.opacity = 0.5 + (Math.random() * 0.5);
            block.style.borderTop = '2px solid white';
            pianoRoll.appendChild(block);
        }
        document.getElementById('composition-log').textContent = 'PLAYING_ALGORITHMIC_MELODY...';
    }
</script>
`;

// CLI Execution if run directly
if (process.argv[1].endsWith('music-factory.js')) {
    console.log('🎵 NetworkBuster Music Factory');
    
    console.log('1. Synthesizing Sound...');
    const wav = generateWav(440, 1, 'sine');
    console.log(`   ✓ Generated: ${wav}`);

    console.log('4. Composing Melody...');
    const melody = composeMelody(16);
    console.log(`   ✓ Notes: ${melody.join(', ')}`);

    console.log('2. Generating MIDI...');
    const midi = generateMidi(melody);
    console.log(`   ✓ Generated: ${midi}`);
    
    console.log('\n🚀 Done! Use server-audio.js to access Web Audio UI.');
}
