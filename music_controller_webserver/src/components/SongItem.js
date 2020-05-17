import React, { Component } from 'react';
import PropTypes from 'prop-types';

import SongButton from "./SongButton";

class SongItem extends Component{
    
    getStyle = () => {
        return {
            background: "#f4f4f4",
            borderBottom: "1px #ccc dotted",
            color: this.props.current_song ? "#4ae072" : "black",
            width: "100%",
            textAlign: "center",
            display: "table-row",
            maxHeight: '100px',
        };
    }

    getRemoveStyle = () => {
        return {
            background: this.props.current_song ? "#f4f4f4" : "red",
            color: this.props.current_song ? "#f4f4f4" : "white",
            height: "100%",
            minWidth: "50px",
            display: "table-cell",
            verticalAlign: "middle",
            fontSize: "30px",
        };
    }

    render(){
        let isSongLoaded = this.props.song_loaded;
        let isSongCurrent = this.props.current_song;
        const renderSong = () => {
            return (
                <div style={this.getStyle()}>
                    {renderSongDetails()}
                    {renderButton()}
                </div>
            );
        }

        const renderSongDetails = () => {
            return isSongLoaded ? [
                <img src={this.props.song.artwork_url} style={songImgStyle} key='0'/>,
                <h1 style={songTitleStyle} key='1'> {this.props.song.title} - {this.props.song.artist}</h1>
            ] : 
                <h1 style={songTitleStyle}> {this.props.song.url} </h1>;
        }

        const renderButton = () => {
            return this.props.current_song ? <SongButton button_type="empty"/> : <SongButton button_type="remove" button_func={this.props.song_mod} remove_key={this.props.song.key}/>;
        }

        return renderSong();
    }
}

SongItem.propTypes = {
    song: PropTypes.object.isRequired,
    current_song: PropTypes.bool.isRequired,
    song_loaded: PropTypes.bool.isRequired,
}

// left
const songImgStyle = {
    marginLeft: '5px',
    maxHeight: '75px',
    display: "table-cell",
    verticalAlign: "middle",
}
// center
const songTitleStyle = {
    display: "table-cell",
    verticalAlign: "middle",
}

export default SongItem;