import React, { Component } from 'react';

class SongItemTitle extends Component{

    render(){
        return(
            <div style={containerStyle}>
                <h1 style={titleStyle}>{this.props.title}</h1>
                <p style={artistStyle}>{this.props.artist}</p>
            </div>
        );
    }
}

const containerStyle = {
    marginLeft: '5px',
}

const artistStyle = {
    color: 'rgb(105, 105, 105)',
    marginLeft: '10px',
    marginTop: '0px',
}

const titleStyle = {
    marginBottom: '3px',
}

export default SongItemTitle;
