import React, { Component } from 'react';
import './App.css';
import axios from 'axios';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Header from "./components/layout/Header";
import SongQueue from "./components/SongQueue";

class App extends Component {

  state = {
    player: {
      "current_song": null,
      "songs": []
    }
  }


  updateState(){
    axios.get('http://localhost:5000/songs').then(
      res => this.setState({player: res.data})
    );
  }

  componentDidMount(){
    this.updateState()
    this.interval = setInterval(() => this.updateState(), 1000);
  }

  componentWillUnmount(){
    clearInterval(this.interval)
  }

  removeSong = key => {
    this.setState({
      player: {
        "current_song": this.state.player["current_song"],
        "songs": [...this.state.player["songs"].filter(song => song.key !== key)]
      }
    })

    // change backend server state
    axios.get(`http://localhost:5000/remove_song/${key}`).then(res =>
    console.log(res.data)
    );
  }

  render() {
    return (
      <Router>
        <div className="App">
          <div className="container">
            <Header />
            <Route exact path="/" render={props => (
              <React.Fragment>
                <SongQueue songs={this.state.player['songs']} current_song={this.state.player['current_song']} song_mod={this.removeSong}/>
              </React.Fragment>
            )}/>
            <Route exact path = "/add" render={props => (
              <React.Fragment>

              </React.Fragment>
            )}/>
          </div>
        </div>
      </Router>
      
    );
  }
}


export default App;
