import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import StartupSound from '../public/startup-sound.mp3'
import './index.css';

let audio = new Audio(StartupSound);
audio.play();

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
