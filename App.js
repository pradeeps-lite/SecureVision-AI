import React, { useState } from 'react';
import './App.css';

function App() {
  const [token, setToken] = useState('');
  const streamUrl = 'http://localhost:5000/api/stream';

  const login = async () => {
    const res = await fetch('http://localhost:5000/api/auth/login', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({username:'admin', password:'admin'})
    });
    const data = await res.json();
    setToken(data.token);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h2>SecureVision AI — Dashboard</h2>
        {!token && <button onClick={login}>Login (demo)</button>}
        {token && (
          <div>
            <p>Live Stream (secured)</p>
            <img
              alt="stream"
              src={streamUrl}
              style={{width:'80%', border:'2px solid #333'}}
            />
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
