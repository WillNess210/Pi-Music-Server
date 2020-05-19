import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

class Header extends Component{

    linkData = [
        {
            title: 'Queue',
            link: "/",
        },
        {
            title: 'Soundcloud Search',
            link: "/add",
        },
        {
            title: 'Will Soundcloud',
            link: "/will",
        },
    ]

    render(){
        return (
            <header style={headerStyle}>
                <h1> Music Player </h1>
                <div style={navStyle}>
                    {this.linkData.map((linkObj, i) => {
                        return <Link className="hoverLink" style={linkStyle} to={linkObj.link}>{linkObj.title}</Link>
                    })}
                    <div className="hoverLink" style={
                        Object.assign({}, linkStyle, {color: this.props.auto_play ? 'rgb(175, 255, 175)' : 'rgb(255, 150, 150)'})
                    } onClick={this.props.toggle_auto_play.bind(this)}>Autoplay {this.props.auto_play ? "On" : "Off"}</div>
                </div>
            </header>
        );
    }
}

const headerStyle = {
    background: '#333',
    color: '#fff',
    textAlign: 'center',
    padding: '10px'
}

const navStyle = {
    width: "100%",
};


const linkStyle = {
    textDecoration: 'none',
    fontSize: "25px",
    display: 'inline-block',
    margin: '5px',
    padding: '5px',
    border: '1px solid gray',
    cursor: 'pointer',
};
  
export default Header;