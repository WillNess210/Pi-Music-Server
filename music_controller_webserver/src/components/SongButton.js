import React, { Component } from 'react';
import PropTypes from 'prop-types';

class SongButton extends Component{

    combineStyles(a, b){
        return Object.assign({}, a, b);
    };

    render(){
        if(this.props.button_type === "remove"){
            return (
                <div className="removeButton" onClick={this.props.button_func.bind(this, this.props.remove_key)} style={buttonContainerStyle}>
                    <div style={xStyle}>x</div>
                </div>
            );
        }else if(this.props.button_type === "empty"){
            return <div style = {this.combineStyles(buttonContainerStyle, emptyStyle)}></div>
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
                        <div style = {xStyle}> > </div>
                    </div>
                    <div className="skipButton" style = {buttonContainerStyle}>
                        <div onClick={this.props.skip_func.bind(this, this.props.song_url)} style={xStyle}> >> </div>
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

const buttonContainerStyle = {
    display: "table",
    verticalAlign: "middle",
    height: "100%",
    width: "100%",
    fontSize: "40px",
    color: "white",
};

const playStyle = {
    background: "gray",
};

const skipStyle = {
    background: "green",
};

const addStyle = {
    background: "green",
};

const emptyStyle = {
    background: "#f4f4f4",
};

SongButton.propTypes = {
    button_type: PropTypes.string.isRequired,
};

export default SongButton;