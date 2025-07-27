import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PlantDetail = ({ match }) => {
    const [plant, setPlant] = useState(null);
    const [history, setHistory] = useState([]);
    const [message, setMessage] = useState('');
    const [image, setImage] = useState(null);

    useEffect(() => {
        const plantId = match.params.id;
        axios.get(`/api/plants/${plantId}`)
            .then(response => {
                setPlant(response.data);
            });
        axios.get(`/api/chat/history/${plantId}`)
            .then(response => {
                setHistory(response.data);
            });
    }, [match.params.id]);

    const sendMessage = () => {
        const plantId = match.params.id;
        const formData = new FormData();
        formData.append('message', message);
        if (image) {
            formData.append('image', image);
        }

        axios.post(`/api/chat/message/${plantId}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(response => {
            setHistory([...history, { role: 'user', content: message }, { role: 'ai', content: response.data }]);
            setMessage('');
            setImage(null);
        });
    };

    if (!plant) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>{plant.nickname}</h2>
            <p>{plant.latinName}</p>
            <div>
                {history.map((item, index) => (
                    <div key={index}>
                        <strong>{item.role}:</strong> {item.content}
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={message}
                onChange={e => setMessage(e.target.value)}
            />
            <input
                type="file"
                onChange={e => setImage(e.target.files[0])}
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default PlantDetail;
