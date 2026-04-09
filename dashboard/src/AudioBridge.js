/**
 * React-compatible AudioBridge for Dashboard
 */

const AUDIO_SERVER = 'http://localhost:3002';

export const initAudioSession = async () => {
    try {
        const response = await fetch(`${AUDIO_SERVER}/api/audio/stream/create`, { method: 'POST' });
        const data = await response.json();
        console.log(`[AudioBridge] Session initialized: ${data.streamId}`);
        return data;
    } catch (error) {
        console.error('[AudioBridge] Failed to init session:', error);
    }
};

export const playTone = async (frequency, duration = 1000, waveform = 'sine') => {
    try {
        const response = await fetch(`${AUDIO_SERVER}/api/audio/synthesize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ frequency, duration, waveform })
        });
        return await response.json();
    } catch (error) {
        console.error('[AudioBridge] Synthesis error:', error);
    }
};

export const getSpectrumData = async (streamId) => {
    if (!streamId) return null;
    try {
        const response = await fetch(`${AUDIO_SERVER}/api/audio/spectrum`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ streamId })
        });
        return await response.json();
    } catch (error) {
        console.error('[AudioBridge] Spectrum error:', error);
    }
};
