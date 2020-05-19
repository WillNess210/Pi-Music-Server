import React, { Component } from 'react';

class EmptyNotification extends Component{
    
    render(){
        return (
            <div style={emptyContainerStyle}>
                <h3 style={messageStyle}>{this.props.message}</h3>
            </div>
        );
    }
}


const emptyContainerStyle = {
    width: "100%",
    textAlign: "center",
}

const messageStyle = {
    color: "rgb(150, 150, 150)",
}


export default EmptyNotification;