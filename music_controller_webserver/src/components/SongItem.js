import React, { Component } from 'react';
import PropTypes from 'prop-types';

import SongButton from "./SongButton";

class SongItem extends Component{
    
   
    render(){
        let isSongLoaded = this.props.song_loaded;
        let isSongCurrent = this.props.current_song;

        const renderImg = () => {
            return isSongLoaded ? <img src={this.props.song.artwork_url} style={songImgStyle}/> : null;
        }

        const renderTitle = () => {
            return isSongLoaded ? <h1> {this.props.song.title} - {this.props.song.artist}</h1> : null;
        }

        const renderInteractButtons = () => {
            if(isSongCurrent){
                return <SongButton button_type="current" play_func={this.props.play_func} skip_func={this.props.skip_func} />
            }else{
                if(this.props.queue_type === "queue"){
                    return <SongButton button_type="remove" button_func={this.props.song_mod} remove_key={this.props.song.key}/>
                }else{
                    return <SongButton button_type="add" song_url={this.props.song.url} button_func={this.props.song_mod}/>
                }
            }
        }

        return(
            <div style = {rowStyle}>
                <div>
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

const singleButtonStyle = {

}

const rowStyle = {
    display: 'grid',
    width: '100%',
    gridTemplateColumns: "5% 85% 10%",
    background: "#f4f4f4",
    borderBottom: "1px #ccc dotted",
}

const songImgStyle = {
    margin: '5px',
    maxHeight: '75px',
    display: "table-cell",
    verticalAlign: "middle",
    
}

SongItem.propTypes = {
    song: PropTypes.object.isRequired,
    current_song: PropTypes.bool.isRequired,
    song_loaded: PropTypes.bool.isRequired,
    queue_type: PropTypes.string.isRequired,
}

export default SongItem;