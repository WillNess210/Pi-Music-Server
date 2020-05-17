import React, { Component } from 'react';
import PropTypes from 'prop-types';

class SongItem extends Component{

    renderLoadedSong = () => {
        return (
            <div style={this.getStyle()}>
                <img src={this.props.song.artwork_url} style={songImgStyle}/>
                <h1 style={songTitleStyle}> {this.props.song.title} - {this.props.song.artist} </h1>
            </div>
        );
    }

    renderUnloadedSong = () => {
        return (
            <div style={this.getStyle()}>
                <h1 style={songTitleStyle}> {this.props.song.url} </h1>
            </div>
        );
    }

    getStyle = () => {
        return {
            background: "#f4f4f4",
            padding: "10px",
            borderBottom: "1px #ccc dotted",
            color: this.props.current_song ? "#4ae072" : "black",
        };
    }

    render(){
        return this.props.song_loaded ? this.renderLoadedSong() : this.renderUnloadedSong();
    }
}

SongItem.propTypes = {
    song: PropTypes.object.isRequired,
}


const songImgStyle = {
    float: 'left',
    display: 'block',
    maxHeight: '75px',
}

const songTitleStyle = {
    textAlign: 'center',
}

export default SongItem;