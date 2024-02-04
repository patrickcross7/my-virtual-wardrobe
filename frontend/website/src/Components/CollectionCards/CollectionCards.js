import "./CollectionCards.css";
import axios from 'axios';
import React, { useState, useEffect } from 'react';


function CollectionCards() {
    const [cards, setCards] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:4000/db/shirts');
                setCards(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
    }, []);



    return (
        <section>
            <div className="container">
                <h1>
                    <div className="cards">
                        {cards.map((card, i) => (
                            <div key={i} className="card">
                                <h3>{card.title}</h3>
                                <img className="image" src={card.image} alt={card.title} />
                                <p>{card.season}</p>
                            </div>
                        ))}
                    </div>
                </h1>
            </div>
        </section>
    );
}

export default CollectionCards;
