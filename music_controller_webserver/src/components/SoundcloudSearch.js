import React, { Component } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

import SongQueue from "./SongQueue";

class SoundcloudSearch extends Component{

    state = {
        search: '',
        current_search: '',
        songs: [],
        last_update:-1,
    }

    onChange = (e) => {
        this.setState({'current_search': e.target.value});
        this.setState({'last_update': Date.now()});
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
                    song_objects.push(this.props.createSongObject(song_results[i], i));
                }
                this.setState({songs: song_objects});
                console.log(this.state.songs)
            }
        );
    };


    componentDidMount(){
        this.interval = setInterval(() => {
            if(this.state.current_search !== this.state.search && Date.now() - this.state.last_update > 500){
                this.setState({
                    search: this.state.current_search,
                    last_update: Date.now(),
                });
                this.searchSoundcloud();
            }
        }, 1000);
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
                    autocomplete="off"
                    autoFocus
                />
                <SongQueue queue_type='add' songs={this.state['songs']} current_song={null} song_mod={this.addSong}/>
            </div>
            
        );
    }
}

const searchStyle = {
    width: "100%",
    height: "50px",
    fontSize: "30px",
    textAlign: "center",
    color: "gray",
}

SoundcloudSearch.propTypes = {
    client_id: PropTypes.string.isRequired,
}

export default SoundcloudSearch;