import React, { Component } from 'react';
import './App.css';
import axios from 'axios';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Header from "./components/layout/Header";
import SongQueue from "./components/SongQueue";
import SoundcloudSearch from './components/SoundcloudSearch';
import SoundcloudFavorites from './components/SoundcloudFavorites';
import SpotifyLanding from './components/SpotifyLanding';
import SpotifyLikes from './components/SpotifyLikes';

class App extends Component {

  state = {
    player: {
      "current_song": null,
      "songs": [],
      "rep": '-1',
      "auto_play": false,
    },
    will_soundcloud_songs: [],
  }


  updateState(){
    let getStr = `/songs/${this.state.player.rep}`;
    console.log(getStr);
    axios.get(`/songs/${this.state.player.rep}`).then(
      res => {
        console.log(res.data);
        if(this.state.player.rep !== res.data.rep){
          this.setState({player: res.data});
          console.log(`Setting state to:`)
          console.log(res.data);
        }
    });
  }

  loadWillSoundcloudLikes(){
    console.log("Added custom songs");
    axios.get('/will_likes').then(
      res => {
        console.log(res);
        this.setState({will_soundcloud_songs: res.data.songs});
      }
    )
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

  componentDidMount(){
    this.loadWillSoundcloudLikes();
    this.updateState();
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
        "auto_play": this.state.player.auto_play,
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
        "rep": this.state.player.rep,
        "auto_play": this.state.player.auto_play,
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

  sendSpotifyKey = (spotify_key) => {
    axios.get(`/send_spotify_key/${spotify_key}`).then(res => {
      console.log(res.data);
    });
  }

  toggleAutoPlay = () => {
    this.setState({
      player: {
        "current_song": this.state.player.current_song,
        "songs": this.state.player.songs,
        "rep": this.state.player.rep,
        "auto_play": !this.state.player.auto_play,
      }
    })
    axios.get("/toggle_autoplay").then(res => {
      console.log(res.data);
    });
  }

  homepageRender = () => {
    return props => (
      <React.Fragment>
        <SongQueue queue_type='queue' songs={this.state.player['songs']} current_song={this.state.player['current_song']} song_mod={this.removeSong} skip_song={this.skipSong} play_pause_func={this.togglePausePlay}/>
      </React.Fragment>
    );
  }

  render() {
    return (
      <Router>
        <div className="App">
          <div className="container">
            <Header auto_play={this.state.player.auto_play} toggle_auto_play={this.toggleAutoPlay}/>
            <Route exact path="/" render={this.homepageRender()}/>
            <Route exact path="/spotify_return" render={props => (
              <React.Fragment>
                <SpotifyLanding send_key_func={this.sendSpotifyKey}/>
              </React.Fragment>
            )}/>
            <Route exact path="/add" render={props => (
              <React.Fragment>
                <SoundcloudSearch client_id={process.env.REACT_APP_SOUNDCLOUD_ID} add_song={this.addSong} createSongObject={this.createSongObject}/>
              </React.Fragment>
            )}/>
            <Route exact path="/will" render={props => (
              <React.Fragment>
                <SoundcloudFavorites songs={this.state.will_soundcloud_songs} add_song={this.addSong}/>
              </React.Fragment>
            )}/>
            <Route exact path="/spotify_likes" render={ props => (
              <React.Fragment>
                <SpotifyLikes contains_spotify_key={this.state.player.connected_to_spotify} spotify_client_id={process.env.REACT_APP_SPOTIFY_CLIENT_ID} redirect_uri={process.env.REACT_APP_REDIRECT_URI} add_song={this.addSong}/>
              </React.Fragment>
            )}/>
          </div>
        </div>
      </Router>
      
    );
  }
}


export default App;
