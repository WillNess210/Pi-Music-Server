import React, { useState, useEffect } from 'react';
//import logo from '../public/logo.svg';
import './App.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">

        ... no changes in this part ...

        <p>The current time is {currentTime}.</p>
      </header>
      <button onClick={() => fetch('/addSongToQueue')}>Play Sound On Server</button>
      <button onClick={() => fetch('/addSoundCloudTrack/786101896')}>Add Soundcloud Song</button>
    </div>
  );
}

export default App;