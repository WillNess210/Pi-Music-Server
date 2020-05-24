import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';


class SpotifyLikes extends Component{
    render(){
        if(!this.props.contains_spotify_key){
            const scopes = 'app-remote-control%20streaming%20user-read-private%20user-read-email%20user-read-playback-state%20user-modify-playback-state%20user-read-currently-playing%20user-library-read'
            const link_url = `https://accounts.spotify.com/authorize?client_id=${this.props.spotify_client_id}&response_type=code&redirect_uri=${this.props.redirect_uri}&scope=${scopes}&state=abcd`
            console.log(`Adding link with URL ${link_url}`)
            return (<a href={link_url}> Click Here to Log into Spotify </a>);
        }
        console.log(`NOT ADDING link with URL`)
        return <h1> Welcome to Spotify! </h1>
    }
}

export default SpotifyLikes;