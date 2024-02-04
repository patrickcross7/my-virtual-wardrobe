import "./CollectionCards.css";

import React, { useState } from 'react';
import pic from './../../Assets/testPics/test.png';

function CollectionCards() {
    const [cards] = useState([
        
        {
        title: "Grey T-shirt",
        text: "A normal t-shirt",
        pic: pic

        },
        {
            title: "Grey T-shirt",
            text: "A normal t-shirt",
            pic: pic
    
        },
        {
            title: "Grey T-shirt",
            text: "A normal t-shirt",
            pic: pic
    
        },
        {
        title: "Grey T-shirt",
        text: "A normal t-shirt",
        pic: pic

        },
        {
            title: "Grey T-shirt",
            text: "A normal t-shirt",
            pic: pic
    
        },
        {
            title: "Grey T-shirt",
            text: "A normal t-shirt",
            pic: pic
    
        },
        {
        title: "Grey T-shirt",
        text: "A normal t-shirt",
        pic: pic

        },
        {
            title: "Grey T-shirt",
            text: "A normal t-shirt",
            pic: pic
    
        },
        {
            title: "Grey T-shirt",
            text: "A normal t-shirt",
            pic: pic
    
        },
        
        

  
        
    
    
    ])    
    return (
        <>
            <section>
                <div className="container">
                    <h1>
                        <div className="cards">
                        {
                            cards.map((card, i) => (
                                <div key={i} className="card">
                                    <h3>
                                        {card.title}
                                        <img className="image" src={card.pic} alt={card.title} />
                                        <p>{card.text}</p>
                                    </h3>
                                </div>

                            ))
                        }                   
                        </div>
                    </h1>
                </div>
            </section>

        </>
    );
}

export default CollectionCards;