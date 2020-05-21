import React, { Component } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

import SongQueue from "./SongQueue";
import CustomItem from './CustomItem';

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

    addRandom = () => {
        let chosen_song = this.state["songs"][Math.floor(Math.random() * this.state["songs"].length)];
        this.props.add_song(chosen_song.url);
    }

    componentDidMount(){
        this.setState({
            songs: this.props.songs,
        })
    }

    render(){
        let shuffle_item = <CustomItem func={this.addRandom} text={'Add Random Song From Likes'}/>; //<ShuffleItem add_random_song={this.addRandom}/>;
        return <SongQueue queue_type='add' songs={this.state['songs']} current_song={null} song_mod={this.addSong} prefix_songitem={shuffle_item}/>
    }

}

export default SoundcloudFavorites;