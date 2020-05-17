import React from 'react';
import { Link } from 'react-router-dom';

function Header(){
    return (
        <header style={headerStyle}>
            <h1> Music Player </h1>
            <Link style={linkStyle} to="/">Queue</Link> | <Link style={linkStyle} to="/add">Add Song</Link>
        </header>
    )
}

const headerStyle = {
    background: '#333',
    color: '#fff',
    textAlign: 'center',
    padding: '10px'
}

const linkStyle = {
    color: '#fff',
    textDecoration: 'none'
}
  
  export default Header;