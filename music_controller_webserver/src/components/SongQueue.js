import React, { Component } from 'react';
import SongItem from './SongItem';
import PropTypes from 'prop-types';


class SongQueue extends Component{
    render(){
        var rows = [];
        
        if(this.props.current_song != null){
            rows.push(<SongItem key={0} song_loaded={song_loaded(this.props.current_song)} current_song={true} song={this.props.current_song} />)
        }

        this.props.songs.map((song, key) => (
            rows.push(<SongItem key={key+1} song_loaded={song_loaded(song)} current_song={false} song={song} />)
        ));

        return rows;
    }
}

SongQueue.propTypes = {
    songs: PropTypes.array.isRequired,
}

function song_loaded(song){
    return 'title' in song;
}

export default SongQueue;