import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
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
        <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
            {/* Header with back button */}
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '30px' }}>
                <Link 
                    to="/" 
                    style={{ 
                        padding: '8px 16px', 
                        backgroundColor: '#6c757d', 
                        color: 'white', 
                        textDecoration: 'none',
                        borderRadius: '4px',
                        marginRight: '20px'
                    }}
                >
                    ← Back to Plants
                </Link>
                <h1 style={{ margin: 0, color: '#2c3e50' }}>🌱 {plant.nickname}</h1>
            </div>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '30px' }}>
                {/* Plant Information Panel */}
                <div style={{ 
                    backgroundColor: '#f8f9fa', 
                    padding: '20px', 
                    borderRadius: '8px',
                    height: 'fit-content'
                }}>
                    <h3 style={{ margin: '0 0 20px 0', color: '#2c3e50' }}>Plant Details</h3>
                    
                    {/* Plant Image */}
                    {plant.image_path && (
                        <div style={{ marginBottom: '20px', textAlign: 'center' }}>
                            <img 
                                src={`/api/images/${plant.image_path}`} 
                                alt={plant.nickname}
                                style={{ 
                                    maxWidth: '100%', 
                                    maxHeight: '300px',
                                    borderRadius: '8px',
                                    border: '1px solid #ddd'
                                }}
                            />
                        </div>
                    )}
                    
                    {/* Plant Names */}
                    <div style={{ marginBottom: '15px' }}>
                        <h4 style={{ margin: '0 0 5px 0', color: '#2c3e50' }}>
                            {plant.nickname}
                        </h4>
                        {plant.latin_name && (
                            <p style={{ 
                                margin: '0 0 5px 0', 
                                color: '#6c757d', 
                                fontStyle: 'italic',
                                fontSize: '14px'
                            }}>
                                {plant.latin_name}
                            </p>
                        )}
                        {plant.english_name && (
                            <p style={{ 
                                margin: '0', 
                                color: '#495057',
                                fontSize: '14px'
                            }}>
                                {plant.english_name}
                            </p>
                        )}
                    </div>
                    
                    {/* Plant Description */}
                    {plant.description && (
                        <div style={{ marginBottom: '15px' }}>
                            <h5 style={{ margin: '0 0 8px 0', color: '#495057' }}>Description</h5>
                            <p style={{ 
                                margin: '0', 
                                color: '#495057',
                                fontSize: '14px',
                                lineHeight: '1.4'
                            }}>
                                {plant.description}
                            </p>
                        </div>
                    )}
                    
                    {/* Care Instructions */}
                    {plant.care_instructions && (
                        <div style={{ marginBottom: '15px' }}>
                            <h5 style={{ margin: '0 0 8px 0', color: '#495057' }}>Care Instructions</h5>
                            <div style={{ 
                                backgroundColor: 'white', 
                                padding: '12px', 
                                borderRadius: '4px',
                                border: '1px solid #e9ecef'
                            }}>
                                <p style={{ 
                                    margin: '0', 
                                    color: '#495057',
                                    fontSize: '14px',
                                    lineHeight: '1.4'
                                }}>
                                    {plant.care_instructions}
                                </p>
                            </div>
                        </div>
                    )}
                    
                    {/* Plant Metadata */}
                    <div style={{ 
                        borderTop: '1px solid #dee2e6', 
                        paddingTop: '15px',
                        fontSize: '12px',
                        color: '#6c757d'
                    }}>
                        <p style={{ margin: '0 0 5px 0' }}>
                            Added: {new Date(plant.created_at).toLocaleDateString()}
                        </p>
                        {plant.updated_at && plant.updated_at !== plant.created_at && (
                            <p style={{ margin: '0' }}>
                                Updated: {new Date(plant.updated_at).toLocaleDateString()}
                            </p>
                        )}
                    </div>
                </div>
                
                {/* Chat Panel */}
                <div>
                    <h3 style={{ margin: '0 0 20px 0', color: '#2c3e50' }}>Chat with {plant.nickname}</h3>
                    
                    {/* Chat History */}
                    <div style={{ 
                        border: '1px solid #dee2e6', 
                        padding: '15px', 
                        height: '400px', 
                        overflowY: 'auto',
                        marginBottom: '20px',
                        backgroundColor: 'white',
                        borderRadius: '8px'
                    }}>
                        {history.length === 0 ? (
                            <div style={{ 
                                textAlign: 'center', 
                                color: '#6c757d',
                                padding: '40px 20px'
                            }}>
                                <p>Start a conversation with {plant.nickname}!</p>
                                <p style={{ fontSize: '14px' }}>
                                    Ask questions about care, health, or upload photos for analysis.
                                </p>
                            </div>
                        ) : (
                            history.map((item, index) => (
                                <div key={index} style={{ 
                                    marginBottom: '15px',
                                    padding: '12px',
                                    backgroundColor: item.role === 'user' ? '#e3f2fd' : '#f8f9fa',
                                    borderRadius: '8px',
                                    border: item.role === 'user' ? '1px solid #bbdefb' : '1px solid #e9ecef'
                                }}>
                                    <div style={{ 
                                        display: 'flex', 
                                        alignItems: 'flex-start', 
                                        gap: '10px'
                                    }}>
                                        <div style={{ 
                                            width: '32px', 
                                            height: '32px', 
                                            borderRadius: '50%',
                                            backgroundColor: item.role === 'user' ? '#2196f3' : '#28a745',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            color: 'white',
                                            fontSize: '14px',
                                            fontWeight: 'bold',
                                            flexShrink: 0
                                        }}>
                                            {item.role === 'user' ? '👤' : '🤖'}
                                        </div>
                                        <div style={{ flex: 1 }}>
                                            <strong style={{ 
                                                color: '#495057',
                                                fontSize: '14px'
                                            }}>
                                                {item.role === 'user' ? 'You' : 'AI Assistant'}
                                            </strong>
                                            <p style={{ 
                                                margin: '5px 0 0 0', 
                                                color: '#495057',
                                                fontSize: '14px',
                                                lineHeight: '1.4'
                                            }}>
                                                {item.content}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                    
                    {/* Message Input */}
                    <div style={{ 
                        border: '1px solid #dee2e6', 
                        padding: '15px', 
                        borderRadius: '8px',
                        backgroundColor: 'white'
                    }}>
                        <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '10px' }}>
                            <input
                                type="text"
                                value={message}
                                onChange={e => setMessage(e.target.value)}
                                placeholder="Ask about your plant..."
                                style={{ 
                                    flex: 1, 
                                    padding: '10px', 
                                    border: '1px solid #ced4da',
                                    borderRadius: '4px',
                                    fontSize: '14px'
                                }}
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
                                padding: '10px 12px', 
                                backgroundColor: '#007bff', 
                                color: 'white', 
                                borderRadius: '4px',
                                cursor: 'pointer',
                                fontSize: '14px'
                            }}>
                                📷
                            </label>
                            <button 
                                onClick={sendMessage} 
                                disabled={loading || !message.trim()}
                                style={{ 
                                    padding: '10px 20px', 
                                    backgroundColor: loading || !message.trim() ? '#6c757d' : '#28a745', 
                                    color: 'white', 
                                    border: 'none',
                                    borderRadius: '4px',
                                    cursor: loading || !message.trim() ? 'not-allowed' : 'pointer',
                                    fontSize: '14px'
                                }}
                            >
                                {loading ? 'Sending...' : 'Send'}
                            </button>
                        </div>
                        
                        {image && (
                            <div style={{ 
                                padding: '10px', 
                                backgroundColor: '#e7f3ff', 
                                borderRadius: '4px',
                                fontSize: '14px',
                                color: '#0056b3'
                            }}>
                                📎 Selected image: {image.name}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PlantDetail;
