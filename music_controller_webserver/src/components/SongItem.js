import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Dimensions } from 'react-native';
const { width } = Dimensions.get('window');


import SongButton from "./SongButton";
import SongItemTitle from "./SongItemTitle";

const songImgContainerStyle = {
    height: '100%',
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
}

class SongItem extends Component{
    
    songImgStyle = () => {
        return {
            margin: '5px',
            maxHeight: width < 700 ? '70px' : '110px'
        }
    }

    rowStyle = () => {
        return {
            display: 'grid',
            width: '100%',
            gridTemplateColumns: width < 700 ? "80px calc(100% - 220px) 140px" : "120px calc(100% - 300px) 180px",
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
            return isSongLoaded ? <img alt={'Song'} src={this.props.song.artwork_url} style={this.songImgStyle()}/> : null;
        }

        const renderTitle = () => {
            return isSongLoaded ? <SongItemTitle title={this.props.song.title} artist={this.props.song.artist} font_size={fontSize}/> : <h1 style={{fontSize: fontSize}}>{this.props.song.url}</h1>;
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



SongItem.propTypes = {
    song: PropTypes.object.isRequired,
    current_song: PropTypes.bool.isRequired,
    song_loaded: PropTypes.bool.isRequired,
    queue_type: PropTypes.string.isRequired,
}

export default SongItem;