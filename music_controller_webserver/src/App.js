import React, { Component } from 'react';
import './App.css';
import axios from 'axios';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Header from "./components/layout/Header";
import SongQueue from "./components/SongQueue";
import SoundcloudSearch from './components/SoundcloudSearch';

class App extends Component {

  state = {
    player: {
      "current_song": null,
      "songs": [],
      "rep": -1,
    },
    will_soundcloud_songs: []
  }


  updateState(){
    axios.get('/songs').then(
      res => {
        if(this.state.player.rep != res.data.rep){
          this.setState({player: res.data});
        }
      });
  }

  createSongObject = (song, key) => {
      return {
          url: song['permalink_url'],
          key: key,
          title: song['title'],
          artist: song['user']['username'],
          artwork_url: song['artwork_url'],
      }
  };

  updateWillSoundcloud(){
    let queryURL = `http://api.soundcloud.com/users/79333503/favorites?client_id=${process.env.REACT_APP_SOUNDCLOUD_ID}`;
    axios.get(queryURL).then(res => {
      let song_results = res.data;
      let song_objects = []
      for(let i = 0; i < song_results.length; i++){
          song_objects.push(this.createSongObject(song_results[i], i));
      }
      this.setState({will_soundcloud_songs: song_objects});
    });
  }

  componentDidMount(){
    this.updateState()
    this.updateWillSoundcloud()
    this.interval = setInterval(() => this.updateState(), 1000);
  }

  componentWillUnmount(){
    clearInterval(this.interval)
  }

  removeSong = key => {
    this.setState({
      player: {
        "current_song": this.state.player["current_song"],
        "songs": [...this.state.player["songs"].filter(song => song.key !== key)],
        "rep": this.state.player.rep,
      }
    });

    // change backend server state
    axios.get(`/remove_song/${key}`).then(res =>
    console.log(res.data)
    );
  }

  addSong = url => {
    axios.get(`/add_song/url=${url}`).then(res =>
      console.log(res.data)
    );
  }

  skipSong = () => {
    this.setState({
      player: {
        "current_song": null,
        "songs": this.state.player.songs,
        "rep": this.state.player.rep
      }
    })
    axios.get("/skip_song").then(res =>{
      console.log(res.data);
    });
  }

  togglePausePlay = () => {
    axios.get("/pause_play").then(res => {
      console.log(res.data);
    });
  }

  render() {
    return (
      <Router>
        <div className="App">
          <div className="container">
            <Header />
            <Route exact path="/" render={props => (
              <React.Fragment>
                <SongQueue queue_type='queue' songs={this.state.player['songs']} current_song={this.state.player['current_song']} song_mod={this.removeSong} skip_song={this.skipSong} play_pause_func={this.togglePausePlay}/>
              </React.Fragment>
            )}/>
            <Route exact path = "/add" render={props => (
              <React.Fragment>
                <SoundcloudSearch client_id={process.env.REACT_APP_SOUNDCLOUD_ID} add_song={this.addSong} createSongObject={this.createSongObject}/>
              </React.Fragment>
            )}/>
            <Route exact path = "/will" render={props => (
              <React.Fragment>
                <SongQueue queue_type='add' songs={this.state.will_soundcloud_songs} current_song={null} song_mod={this.addSong}/>
              </React.Fragment>
            )}/>
          </div>
        </div>
      </Router>
      
    );
  }
}


export default App;
