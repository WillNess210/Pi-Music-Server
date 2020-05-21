import React, { Component } from 'react';

const containerStyle = {
    marginLeft: '5px',
}

class SongItemTitle extends Component{

    titleStyle = () => {
        return {
            marginBottom: '3px',
            fontSize: this.props.font_size,
        }
    }

    artistStyle = () => {
        return {
            color: 'rgb(105, 105, 105)',
            marginLeft: '10px',
            marginTop: '0px',
            fontSize: this.props.font_size/1.5,
        }
    }

    render(){
        return(
            <div style={containerStyle}>
                <h1 style={this.titleStyle()}>{this.props.title}</h1>
                <h2 style={this.artistStyle()}>{this.props.artist}</h2>
            </div>
        );
    }
}




export default SongItemTitle;
