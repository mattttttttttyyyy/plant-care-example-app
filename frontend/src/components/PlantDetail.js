import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const PlantDetail = () => {
    const { id } = useParams();
    const [plant, setPlant] = useState(null);
    const [history, setHistory] = useState([]);
    const [message, setMessage] = useState('');
    const [image, setImage] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const plantId = id;
        axios.get(`/api/plants/${plantId}`)
            .then(response => {
                setPlant(response.data);
            })
            .catch(error => {
                console.error('Error fetching plant:', error);
            });
        
        axios.get(`/api/chat/history/${plantId}`)
            .then(response => {
                setHistory(response.data);
            })
            .catch(error => {
                console.error('Error fetching chat history:', error);
            });
    }, [id]);

    const sendMessage = async () => {
        if (!message.trim()) return;
        
        setLoading(true);
        const plantId = id;
        
        try {
            // Prepare request data
            const requestData = {
                message: message
            };
            
            // Add image if selected
            if (image) {
                const reader = new FileReader();
                reader.onload = async () => {
                    const base64Image = reader.result;
                    requestData.image = base64Image;
                    
                    await sendRequest(requestData, plantId);
                };
                reader.readAsDataURL(image);
            } else {
                await sendRequest(requestData, plantId);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            setLoading(false);
        }
    };

    const sendRequest = async (requestData, plantId) => {
        try {
            const response = await axios.post(`/api/chat/message/${plantId}`, requestData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            // Add user message and AI response to history
            const newHistory = [
                ...history,
                { role: 'user', content: message },
                { role: 'assistant', content: response.data.response }
            ];
            
            setHistory(newHistory);
            setMessage('');
            setImage(null);
            setLoading(false);
        } catch (error) {
            console.error('Error sending message:', error);
            setLoading(false);
        }
    };

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            // Check file size (16MB limit)
            if (file.size > 16 * 1024 * 1024) {
                alert('Image size must be less than 16MB');
                return;
            }
            
            // Check file type
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
            if (!allowedTypes.includes(file.type)) {
                alert('Please select a valid image file (JPEG, PNG, GIF)');
                return;
            }
            
            setImage(file);
        }
    };

    if (!plant) {
        return <div style={{ padding: '20px', textAlign: 'center' }}>Loading...</div>;
    }

    return (
        <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
            <h2>{plant.nickname}</h2>
            {plant.latin_name && <p><em>{plant.latin_name}</em></p>}
            
            {plant.image_path && (
                <div style={{ marginBottom: '20px' }}>
                    <img 
                        src={`/api/images/${plant.image_path}`} 
                        alt={plant.nickname}
                        style={{ maxWidth: '300px', maxHeight: '300px' }}
                    />
                </div>
            )}
            
            <div style={{ 
                border: '1px solid #ccc', 
                padding: '10px', 
                height: '300px', 
                overflowY: 'auto',
                marginBottom: '20px'
            }}>
                {history.map((item, index) => (
                    <div key={index} style={{ 
                        marginBottom: '10px',
                        padding: '8px',
                        backgroundColor: item.role === 'user' ? '#e3f2fd' : '#f5f5f5',
                        borderRadius: '4px'
                    }}>
                        <strong>{item.role === 'user' ? 'You' : 'AI'}:</strong> {item.content}
                    </div>
                ))}
            </div>
            
            <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                <input
                    type="text"
                    value={message}
                    onChange={e => setMessage(e.target.value)}
                    placeholder="Ask about your plant..."
                    style={{ flex: 1, padding: '8px' }}
                    onKeyPress={e => e.key === 'Enter' && sendMessage()}
                />
                <input
                    type="file"
                    onChange={handleImageChange}
                    accept="image/*"
                    style={{ display: 'none' }}
                    id="image-input"
                />
                <label htmlFor="image-input" style={{ 
                    padding: '8px 12px', 
                    backgroundColor: '#007bff', 
                    color: 'white', 
                    borderRadius: '4px',
                    cursor: 'pointer'
                }}>
                    📷
                </label>
                <button 
                    onClick={sendMessage} 
                    disabled={loading || !message.trim()}
                    style={{ 
                        padding: '8px 16px', 
                        backgroundColor: '#28a745', 
                        color: 'white', 
                        border: 'none',
                        borderRadius: '4px',
                        cursor: loading ? 'not-allowed' : 'pointer'
                    }}
                >
                    {loading ? 'Sending...' : 'Send'}
                </button>
            </div>
            
            {image && (
                <div style={{ marginTop: '10px' }}>
                    <p>Selected image: {image.name}</p>
                </div>
            )}
        </div>
    );
};

export default PlantDetail;
