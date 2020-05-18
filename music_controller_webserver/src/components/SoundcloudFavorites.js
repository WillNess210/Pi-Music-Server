import React, { Component } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

import SongQueue from "./SongQueue";

class SoundcloudFavorites extends Component{

    state = {
        songs: [],
    };


    updateWillSoundcloud(){
        let queryURL = `http://api.soundcloud.com/users/${this.props.soundcloud_user_id}/favorites?client_id=${this.props.client_id}&limit=200`;
        axios.get(queryURL).then(res => {
          let song_results = res.data;
          let song_objects = []
          for(let i = 0; i < song_results.length; i++){
              song_objects.push(this.props.createSongObject(song_results[i], i));
          }
          this.setState({songs: song_objects});
        });
      }

    addSong = (track_url) => {
        // remove song locally
        this.setState({
            songs: [...this.state["songs"].filter(song => song.url !== track_url)]
        });
        // add song to server
        this.props.add_song(track_url);
    }

    componentDidMount(){
        this.updateWillSoundcloud();
    }

    render(){
        return <SongQueue queue_type='add' songs={this.state['songs']} current_song={null} song_mod={this.addSong}/>
    }

}

export default SoundcloudFavorites;