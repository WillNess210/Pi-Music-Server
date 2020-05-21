import React, { Component } from 'react';
import { Dimensions } from 'react-native';
const { width } = Dimensions.get('window');

const rowStyle = {
    width: '100%',
    borderBottom: "1px #ccc dotted",
    minHeight: '85px',
    textAlign: 'center',
    marginTop: '0px',
    display: 'table',
    cursor: 'pointer',
}

class CustomItem extends Component{
    
    textStyle = () => {
        let fontSize = width < 700 ? 20 : 40;
        return {
            width: '100%',
            fontSize: fontSize,
            display: 'table-cell',
            verticalAlign: 'middle',
            color: 'rgb(75, 75, 75)',
        }
    }
   
    render(){
        return(
            <div className='customButton' style={rowStyle} onClick={this.props.func.bind(this)}>
                <h1 style={this.textStyle()}>{this.props.text}</h1>
            </div>
        );

    }
}


export default CustomItem;