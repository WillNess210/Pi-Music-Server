import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

class SpotifyLanding extends Component{
    render(){
        let search = window.location.search;
        let params = new URLSearchParams(search);
        let spotify_key = params.get('code');
        console.log(`GOT SPOTIFY KEY |${spotify_key}|`);
        this.props.send_key_func(spotify_key)
        //return(<h1> You should redirect soon :) </h1>);
        return (<Redirect to='/' />)
    }
}


export default SpotifyLanding;