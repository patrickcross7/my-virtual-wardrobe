import "./NavBarStyle.css";

import React, { useState } from 'react';


function Navbar() {

    return (
        <>
                <div className="navbar">    
                    <li> 
                        <a className="collection" href="/collections">
                            Collections
                        </a>
                    </li>   

                    <li> 
                        <a className="home" href="/">
                            Home
                        </a>
                    </li>                       
                </div>

        </>
    );
}

export default Navbar;