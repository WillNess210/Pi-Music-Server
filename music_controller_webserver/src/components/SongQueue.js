import React, { Component } from 'react';
import SongItem from './SongItem';
import PropTypes from 'prop-types';
import EmptyNotification from './EmptyNotification';

const songQueueStyle = {
    display: "table",
    width: "100%",
    borderCollapse: "collapse",
}

class SongQueue extends Component{
    
    render(){
        var rows = [];

        if(this.props.prefix_songitem != null){
            rows.push(this.props.prefix_songitem);
        }
        
        if(this.props.current_song != null){
            rows.push(<SongItem key={this.props.current_song['key']} song_loaded={song_loaded(this.props.current_song)} current_song={true} song={this.props.current_song} play_func={this.props.play_pause_func} skip_func={this.props.skip_song} queue_type={this.props.queue_type}/>);
        }

        this.props.songs.map((song) => (
            rows.push(<SongItem key={song['key']} song_loaded={song_loaded(song)} current_song={false} song={song} song_mod={this.props.song_mod} queue_type={this.props.queue_type}/>)
        ));

        if(this.props.current_song === null && this.props.songs.length === 0){
            let empty_msg = {
                queue: 'No songs currently in queue.',
                add: 'No songs found.'
            }[this.props.queue_type];
            return <EmptyNotification message={empty_msg}/>;
        }

        return (
            <div style={songQueueStyle}> 
                {rows}
            </div>
        );
        
    }
}

SongQueue.propTypes = {
    songs: PropTypes.array.isRequired,
    //current_song: PropTypes.object.isRequired,
    song_mod: PropTypes.func.isRequired,
    queue_type: PropTypes.string.isRequired,
}

function song_loaded(song){
    return 'title' in song;
}


export default SongQueue;