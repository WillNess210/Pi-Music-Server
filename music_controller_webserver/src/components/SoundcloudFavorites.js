import React, { Component } from 'react';

import SongQueue from "./SongQueue";
import CustomItem from './CustomItem';

class SoundcloudFavorites extends Component{

    constructor(props){
        super(props);
        
        this.state = {
            songs: [],
            all_songs: [],
            hasMore: true,
            isLoading: false,
            error: false,
            cur_index: 0,
        };

        window.onscroll = () => {
            const{
                loadSongs,
                state: {
                    error,
                    isLoading,
                    hasMore,
                },
            } = this;
    
            if(error || isLoading || !hasMore) return;
    
            if(window.innerHeight + document.documentElement.scrollTop === document.documentElement.offsetHeight){
                loadSongs();
            }
        };
    }

    

    addSong = (track_url) => {
        // remove song locally
        this.setState({
            songs: [...this.state["songs"].filter(song => song.url !== track_url)]
        });
        // add song to server
        this.props.add_song(track_url);
    }

    addRandom = () => {
        let chosen_song = this.state["songs"][Math.floor(Math.random() * this.state["songs"].length)];
        this.props.add_song(chosen_song.url);
    }

    componentDidMount(){
        this.setState({
            songs: [],
            all_songs: this.props.songs,
            hasMore: this.props.songs.length > 0,
            isLoading: false,
            error: false,
        })
        this.loadSongs()
    }

    loadSongs = () => {
        console.log('Loading Songs');
        this.setState({ isLoading : true }, () =>{ 
            const nextSongs = this.state.all_songs.slice(this.state.cur_index, 20);
            if(nextSongs.length === 0){
                this.setState({hasMore: false});
                console.log('Ran out of Favorited Songs');
                return;
            }
            const nextStateSongs = [...this.state.songs, ...nextSongs];
            this.setState({ 
                cur_index : this.state.cur_index + 20,
                isLoading : false,
                songs: nextStateSongs,
            });
        })
    }
    

    render(){
        let shuffle_item = <CustomItem key={-1} func={this.addRandom} text={'Add Random Song From Likes'}/>; //<ShuffleItem add_random_song={this.addRandom}/>;
        return <SongQueue queue_type='add' songs={this.state.songs} current_song={null} song_mod={this.addSong} prefix_songitem={shuffle_item}/>
    }

}

export default SoundcloudFavorites;