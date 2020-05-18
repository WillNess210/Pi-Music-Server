import React, { Component } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

import SongQueue from "./SongQueue";

class SoundcloudFavorites extends Component{

    state = {
        songs: [],
    };

    addSong = (track_url) => {
        // remove song locally
        this.setState({
            songs: [...this.state["songs"].filter(song => song.url !== track_url)]
        });
        // add song to server
        this.props.add_song(track_url);
    }

    componentDidMount(){
        this.setState({
            songs: this.props.songs,
        })
    }

    render(){
        return <SongQueue queue_type='add' songs={this.state['songs']} current_song={null} song_mod={this.addSong}/>
    }

}

export default SoundcloudFavorites;