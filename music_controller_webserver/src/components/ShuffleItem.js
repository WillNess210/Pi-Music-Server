import React, { Component } from 'react';
import { Dimensions } from 'react-native';
const { width, height } = Dimensions.get('window');

class ShuffleItem extends Component{
    
    textStyle = () => {
        let fontSize = width < 700 ? 20 : 40;
        return {
            width: '100%',
            fontSize: fontSize,
            display: 'table-cell',
            verticalAlign: 'middle',
        }
    }
   
    render(){
        return(
            <div className='shuffleButton' style={rowStyle} onClick={this.props.add_random_song.bind(this)}>
                <h1 style={this.textStyle()}>Add Random Song From Likes</h1>
            </div>
        );

    }
}

const rowStyle = {
    width: '100%',
    borderBottom: "1px #ccc dotted",
    minHeight: '85px',
    textAlign: 'center',
    marginTop: '0px',
    display: 'table',
    cursor: 'pointer',
}

export default ShuffleItem;