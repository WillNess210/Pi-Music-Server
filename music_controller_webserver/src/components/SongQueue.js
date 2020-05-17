import React, { Component } from 'react';
import SongItem from './SongItem';
import PropTypes from 'prop-types';


class SongQueue extends Component{
    render(){
        var rows = [];
        
        if(this.props.current_song != null){
            rows.push(<SongItem key={this.props.current_song['key']} song_loaded={song_loaded(this.props.current_song)} current_song={true} song={this.props.current_song} song_mod={this.props.skip_song}/>)
        }

        this.props.songs.map((song) => (
            rows.push(<SongItem key={song['key']} song_loaded={song_loaded(song)} current_song={false} song={song} song_mod={this.props.song_mod} queue_type={this.props.queue_type}/>)
        ));

        return (
            <div style = {songQueueStyle}> 
                {rows}
            </div>
        );
    }
}

SongQueue.propTypes = {
    songs: PropTypes.array.isRequired,
    current_song: PropTypes.object.isRequired,
    song_mod: PropTypes.func.isRequired,
    queue_type: PropTypes.string.isRequired,
}

function song_loaded(song){
    return 'title' in song;
}

const songQueueStyle = {
    display: "table",
    width: "100%",
    borderCollapse: "collapse",
}

export default SongQueue;