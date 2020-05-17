import React, { Component } from 'react';
import PropTypes from 'prop-types';

class SongButton extends Component{
    render(){
        if(this.props.button_type === "remove"){
            return <div onClick={this.props.button_func.bind(this, this.props.remove_key)} style={removeStyle}> x </div>
        }else if(this.props.button_type === "empty"){
            return <div style = {emptyStyle}></div>
        }else if(this.props.button_type === "add"){
            return <div onClick={this.props.button_func.bind(this, this.props.song_url)} style={addStyle}> + </div>
        }else if(this.props.button_type === "skip"){
            return <div onClick={this.props.button_func.bind(this, this.props.song_url)} style={skipStyle}> >> </div>
        }
        return <p> you messed up</p>
    }
}


const removeStyle = {
    background: "red",
    color: "white",
    height: "100%",
    minWidth: "50px",
    maxWidth: "50px",
    display: "table-cell",
    verticalAlign: "middle",
    fontSize: "30px",
};

const addStyle = {
    background: "green",
    color: "white",
    height: "100%",
    minWidth: "50px",
    maxWidth: "50px",
    display: "table-cell",
    verticalAlign: "middle",
    fontSize: "30px",
};

const skipStyle = addStyle;

const emptyStyle = {
    background: "#f4f4f4",
    height: "100%",
    minWidth: "50px",
    maxWidth: "50px",
    display: "table-cell",
    verticalAlign: "middle",
    fontSize: "30px",
}

SongButton.propTypes = {
    button_type: PropTypes.string.isRequired,
}

export default SongButton;