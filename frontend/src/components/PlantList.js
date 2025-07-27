import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PlantList = () => {
    const [plants, setPlants] = useState([]);
    const [newPlant, setNewPlant] = useState({ nickname: '', latinName: '' });

    useEffect(() => {
        axios.get('/api/plants')
            .then(response => {
                setPlants(response.data);
            });
    }, []);

    const addPlant = () => {
        axios.post('/api/plants', newPlant)
            .then(response => {
                setPlants([...plants, response.data]);
                setNewPlant({ nickname: '', latinName: '' });
            });
    };

    const removePlant = (id) => {
        axios.delete(`/api/plants/${id}`)
            .then(() => {
                setPlants(plants.filter(plant => plant.id !== id));
            });
    };

    return (
        <div>
            <h2>Plants</h2>
            <ul>
                {plants.map(plant => (
                    <li key={plant.id}>
                        {plant.nickname} ({plant.latinName})
                        <button onClick={() => removePlant(plant.id)}>Remove</button>
                        <a href={`/plant/${plant.id}`}>Details</a>
                    </li>
                ))}
            </ul>
            <input
                type="text"
                placeholder="Nickname"
                value={newPlant.nickname}
                onChange={e => setNewPlant({ ...newPlant, nickname: e.target.value })}
            />
            <input
                type="text"
                placeholder="Latin Name"
                value={newPlant.latinName}
                onChange={e => setNewPlant({ ...newPlant, latinName: e.target.value })}
            />
            <button onClick={addPlant}>Add Plant</button>
        </div>
    );
};

export default PlantList;
