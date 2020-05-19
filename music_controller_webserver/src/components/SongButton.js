import React, { Component } from 'react';
import PropTypes from 'prop-types';

class SongButton extends Component{

    

    render(){
        if(this.props.button_type === "remove"){
            return (
                <div className="removeButton" onClick={this.props.button_func.bind(this, this.props.remove_key)} style={buttonContainerStyle}>
                    <div style={getButtonStyle(deleteImg)}></div>
                </div>
            );
        }else if(this.props.button_type === "empty"){
            return <div style = {Object.assign({}, buttonContainerStyle, emptyStyle)}></div>
        }else if(this.props.button_type === "add"){
            return (
                <div className="greenButton" onClick={this.props.button_func.bind(this, this.props.song_url)} style={buttonContainerStyle}>
                    <div style={xStyle}>+</div>
                </div>
            );
        }else if(this.props.button_type === "current"){

            return (
                <div style={currentContainerStyle}>
                    <div className="greenButton" style = {buttonContainerStyle}>
                        <div onClick={this.props.play_func.bind(this)} style = {this.props.cur_playing ? getButtonStyle(pauseImg) : getButtonStyle(playImg)}></div>
                    </div>
                    <div className="skipButton" style = {buttonContainerStyle}>
                        <div onClick={this.props.skip_func.bind(this, this.props.song_url)} style={getButtonStyle(skipImg)}></div>
                    </div>
                </div>
                
            );
        }
        return <p> you messed up</p>
    }
}

const currentContainerStyle = {
    display: "grid",
    gridTemplateColumns: "50% 50%",
    width: "100%",
    height: "100%",
};


const xStyle = {
    display: "table-cell",
    verticalAlign: "middle",
    textAlign: "center",
    minWidth: "100%",
    minHeight: "100%",
};

const skipImg = require('./res/skip_white.png')
const playImg = require('./res/play_white.png')
const pauseImg = require('./res/pause_white.png')
const deleteImg = require('./res/delete_white.png')

function getButtonStyle(img){
    return Object.assign({}, xStyle, {
        backgroundImage: `url(${img})`,
        backgroundSize: "100%",
        backgroundPosition: "center center",
        backgroundRepeat: "no-repeat",
    });
}


const buttonContainerStyle = {
    display: "table",
    verticalAlign: "middle",
    height: "100%",
    width: "100%",
    fontSize: "40px",
    color: "white",
    cursor: 'pointer',
};

const emptyStyle = {
    background: "#f4f4f4",
};

SongButton.propTypes = {
    button_type: PropTypes.string.isRequired,
};

export default SongButton;