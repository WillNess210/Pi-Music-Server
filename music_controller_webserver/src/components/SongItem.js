import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Dimensions } from 'react-native';
const { width, height } = Dimensions.get('window');


import SongButton from "./SongButton";

class SongItem extends Component{
    
    rowStyle = () => {
        return {
            display: 'grid',
            width: '100%',
            gridTemplateColumns: width < 700 ? "80px calc(100% - 220px) 140px" : "80px calc(100% - 260px) 180px",
            background: "rgb(240, 240, 240)",
            borderBottom: "1px #ccc dotted",
            minHeight: '85px',
        }
    };
   
    render(){
        let isSongLoaded = this.props.song_loaded;
        let isSongCurrent = this.props.current_song;

        let fontSize = width < 700 ? 20 : 40;

        

        const renderImg = () => {
            return isSongLoaded ? <img src={this.props.song.artwork_url} style={songImgStyle}/> : null;
        }

        const renderTitle = () => {
            return isSongLoaded ? <h1 style = {{fontSize: fontSize}}> {this.props.song.title} - {this.props.song.artist}</h1> : <h1 style = {{fontSize: fontSize}}>{this.props.song.url}</h1>;
        }

        const renderInteractButtons = () => {
            if(isSongCurrent){
                return <SongButton button_type="current" play_func={this.props.play_func} skip_func={this.props.skip_func} cur_playing={this.props.song.playing} font_size={fontSize}/>
            }else{
                if(this.props.queue_type === "queue"){
                    return <SongButton button_type="remove" button_func={this.props.song_mod} remove_key={this.props.song.key} font_size={fontSize}/>
                }else{
                    return <SongButton button_type="add" song_url={this.props.song.url} button_func={this.props.song_mod} font_size={fontSize}/>
                }
            }
        }

        return(
            <div style={this.rowStyle()}>
                <div style={songImgContainerStyle}>
                    {renderImg()}
                </div>
                <div>
                    {renderTitle()}
                </div>
                <div>
                    {renderInteractButtons()}
                </div>
            </div>
        );

    }
}

const songImgStyle = {
    margin: '5px',
    maxHeight: '75px',
    position: 'absolute',
    top: '0',
    bottom: '0',
    left: '0',
    right: '0',
    margin: 'auto',
}

const songImgContainerStyle = {
    height: "100%",
    width: "100%",
    position: "relative",
}

SongItem.propTypes = {
    song: PropTypes.object.isRequired,
    current_song: PropTypes.bool.isRequired,
    song_loaded: PropTypes.bool.isRequired,
    queue_type: PropTypes.string.isRequired,
}

export default SongItem;