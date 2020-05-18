import React from 'react';
import { Link } from 'react-router-dom';

function Header(){
    const linkData = [
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
    return (
        <header style={headerStyle}>
            <h1> Music Player </h1>
            <div style={navStyle}>
                {linkData.map((linkObj, i) => {
                    return <Link className="hoverLink" style={linkStyle} to={linkObj.link}>{linkObj.title}</Link>
                })}
            </div>
            
        </header>
    )
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
    display: 'inline',
    margin: '5px',
    padding: '5px',
};
  
  export default Header;