import React, { useEffect, useState } from 'react';
import './App.css';
import { initAudioSession, playTone, getSpectrumData } from './AudioBridge';

function App() {
  const [streamId, setStreamId] = useState(null);
  const [spectrum, setSpectrum] = useState(null);

  useEffect(() => {
    const setup = async () => {
      const data = await initAudioSession();
      if (data) setStreamId(data.streamId);
    };
    setup();
  }, []);

  useEffect(() => {
    if (!streamId) return;
    const interval = setInterval(async () => {
      const data = await getSpectrumData(streamId);
      if (data && data.success) setSpectrum(data.spectrum);
    }, 3000);
    return () => clearInterval(interval);
  }, [streamId]);

  const handleAlert = () => {
    playTone(440, 1000, 'sine');
  };

  return (
    <div className="container">
      <h1>Vercel Admin Dashboard</h1>
      <p>Welcome to the Vercel admin template. Use this dashboard to manage your deployments and settings.</p>
      
      <div className="admin-panel">
        <h2>Audio Telemetry (Port 3002)</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '10px', marginBottom: '15px' }}>
          <div className="stat-card">
            <span>Bass</span>
            <strong>{spectrum?.bass || '0.00'}</strong>
          </div>
          <div className="stat-card">
            <span>Mid</span>
            <strong>{spectrum?.mid || '0.00'}</strong>
          </div>
          <div className="stat-card">
            <span>Treble</span>
            <strong>{spectrum?.treble || '0.00'}</strong>
          </div>
        </div>
        <button onClick={handleAlert} className="alert-btn">Test Security Alert Tone</button>
      </div>

      <div className="admin-panel">
        <h2>Project Overview</h2>
        <ul>
          <li>Environment: <strong>Production</strong></li>
          <li>Status: <strong>Online</strong></li>
          <li>Last Deploy: <strong>Just now</strong></li>
          <li>External Link: <a href="https://github.com/Cleanskiier27/luna.eu" target="_blank">luna.eu</a></li>
        </ul>
      </div>
    </div>
  );
}

export default App;
