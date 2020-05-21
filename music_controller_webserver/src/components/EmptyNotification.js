import React, { Component } from 'react';


const emptyContainerStyle = {
    width: "100%",
    textAlign: "center",
}

const messageStyle = {
    color: "rgb(150, 150, 150)",
}

class EmptyNotification extends Component{
    
    render(){
        return (
            <div style={emptyContainerStyle}>
                <h3 style={messageStyle}>{this.props.message}</h3>
            </div>
        );
    }
}



export default EmptyNotification;