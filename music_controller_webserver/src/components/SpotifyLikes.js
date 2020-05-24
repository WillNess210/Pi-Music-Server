import React, { Component } from 'react';
import SongQueue from './SongQueue';
import axios from 'axios';


class SpotifyLikes extends Component{

    addSong = (track_url) => {
        // remove song locally
        this.setState({
            songs: [...this.state["songs"].filter(song => song.url !== track_url)]
        });
        // add song to server
        this.props.add_song(track_url);
    }

    loadSongs = () => {
        axios.get('/spotify_likes').then(
            res => {
                console.log(res);
                this.setState({songs: res.data.songs});
            }
        );
    }

    componentDidMount(){
        this.setState({
            songs: [],
        });
        this.loadSongs();
    }

    render(){
        if(!this.props.contains_spotify_key){
            const scopes = 'app-remote-control%20streaming%20user-read-private%20user-read-email%20user-read-playback-state%20user-modify-playback-state%20user-read-currently-playing%20user-library-read'
            const link_url = `https://accounts.spotify.com/authorize?client_id=${this.props.spotify_client_id}&response_type=code&redirect_uri=${this.props.redirect_uri}&scope=${scopes}&state=abcd`
            console.log(`Adding link with URL ${link_url}`)
            return (<a href={link_url}> Click Here to Log into Spotify </a>);
        }
        console.log(`NOT ADDING link with URL`)
        return <SongQueue queue_type='add' songs={this.state.songs} current_song={null} song_mod={this.addSong} />
    }
}

export default SpotifyLikes;