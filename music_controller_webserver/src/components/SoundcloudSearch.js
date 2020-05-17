import React, { Component } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

import SongQueue from "./SongQueue";

class SoundcloudSearch extends Component{

    state = {
        search: '',
        current_search: '',
        songs: [],
    }

    onChange = (e) => this.setState({'current_search': e.target.value});

    createSongObject = (song, key) => {
        return {
            url: song['permalink_url'],
            key: key,
            title: song['title'],
            artist: song['user']['username'],
            artwork_url: song['artwork_url'],
        }
    };

    addSong = (track_url) => {
        // remove song locally
        this.setState({
            songs: [...this.state["songs"].filter(song => song.url !== track_url)]
        });
        // add song to server
        this.props.add_song(track_url);
    }

    searchSoundcloud = () => {
        let search_url = `http://api.soundcloud.com/tracks?q=${encodeURIComponent(this.state.search)}&client_id=${this.props.client_id}`;
        axios.get(search_url).then(
            res => {
                let song_results = res.data;
                let song_objects = []
                for(let i = 0; i < song_results.length; i++){
                    song_objects.push(this.createSongObject(song_results[i], i));
                }
                this.setState({songs: song_objects});
                console.log(this.state.songs)
            }
        );
    };


    componentDidMount(){
        this.interval = setInterval(() => {
            if(this.state.current_search !== this.state.search){
                this.setState({
                    search: this.state.current_search,
                });
                this.searchSoundcloud();
            }
        }, 2000);
    }
    
    componentWillUnmount(){
        clearInterval(this.interval)
    }

    render(){
        return(
            <div>
                <input
                    type="text"
                    name="soundcloud_search"
                    style={searchStyle}
                    value={this.state.current_search}
                    onChange={this.onChange}
                />
                <SongQueue queue_type='add' songs={this.state['songs']} current_song={null} song_mod={this.addSong}/>
            </div>
            
        );
    }
}

const searchStyle = {
    width: "100%",
}

SoundcloudSearch.propTypes = {
    client_id: PropTypes.string.isRequired,
}

export default SoundcloudSearch;