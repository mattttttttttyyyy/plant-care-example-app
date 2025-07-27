import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PlantList = () => {
    const [plants, setPlants] = useState([]);
    const [newPlant, setNewPlant] = useState({ nickname: '', latin_name: '' });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchPlants();
    }, []);

    const fetchPlants = async () => {
        try {
            setLoading(true);
            const response = await axios.get('/api/plants');
            setPlants(response.data);
            setError(null);
        } catch (error) {
            console.error('Error fetching plants:', error);
            setError('Failed to load plants');
        } finally {
            setLoading(false);
        }
    };

    const addPlant = async () => {
        if (!newPlant.nickname.trim()) {
            alert('Please enter a plant nickname');
            return;
        }

        try {
            const response = await axios.post('/api/plants', newPlant);
            setPlants([...plants, response.data]);
            setNewPlant({ nickname: '', latin_name: '' });
            setError(null);
        } catch (error) {
            console.error('Error adding plant:', error);
            setError('Failed to add plant');
        }
    };

    const removePlant = async (id) => {
        if (!window.confirm('Are you sure you want to delete this plant?')) {
            return;
        }

        try {
            await axios.delete(`/api/plants/${id}`);
            setPlants(plants.filter(plant => plant.id !== id));
            setError(null);
        } catch (error) {
            console.error('Error removing plant:', error);
            setError('Failed to remove plant');
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            addPlant();
        }
    };

    if (loading) {
        return <div style={{ padding: '20px', textAlign: 'center' }}>Loading plants...</div>;
    }

    return (
        <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
            <h1 style={{ color: '#2c3e50', marginBottom: '30px' }}>🌱 Plant Care</h1>
            
            {error && (
                <div style={{ 
                    padding: '10px', 
                    backgroundColor: '#f8d7da', 
                    color: '#721c24', 
                    borderRadius: '4px',
                    marginBottom: '20px'
                }}>
                    {error}
                </div>
            )}
            
            <div style={{ 
                backgroundColor: '#f8f9fa', 
                padding: '20px', 
                borderRadius: '8px',
                marginBottom: '30px'
            }}>
                <h3>Add New Plant</h3>
                <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
                    <input
                        type="text"
                        placeholder="Plant nickname"
                        value={newPlant.nickname}
                        onChange={e => setNewPlant({ ...newPlant, nickname: e.target.value })}
                        onKeyPress={handleKeyPress}
                        style={{ 
                            flex: 1, 
                            padding: '8px', 
                            border: '1px solid #ddd',
                            borderRadius: '4px'
                        }}
                    />
                    <input
                        type="text"
                        placeholder="Latin name (optional)"
                        value={newPlant.latin_name}
                        onChange={e => setNewPlant({ ...newPlant, latin_name: e.target.value })}
                        onKeyPress={handleKeyPress}
                        style={{ 
                            flex: 1, 
                            padding: '8px', 
                            border: '1px solid #ddd',
                            borderRadius: '4px'
                        }}
                    />
                    <button 
                        onClick={addPlant}
                        disabled={!newPlant.nickname.trim()}
                        style={{ 
                            padding: '8px 16px', 
                            backgroundColor: '#28a745', 
                            color: 'white', 
                            border: 'none',
                            borderRadius: '4px',
                            cursor: newPlant.nickname.trim() ? 'pointer' : 'not-allowed'
                        }}
                    >
                        Add Plant
                    </button>
                </div>
            </div>
            
            <div>
                <h3>Your Plants ({plants.length})</h3>
                {plants.length === 0 ? (
                    <div style={{ 
                        textAlign: 'center', 
                        padding: '40px', 
                        color: '#6c757d',
                        backgroundColor: '#f8f9fa',
                        borderRadius: '8px'
                    }}>
                        No plants yet. Add your first plant above!
                    </div>
                ) : (
                    <div style={{ display: 'grid', gap: '15px' }}>
                        {plants.map(plant => (
                            <div key={plant.id} style={{ 
                                border: '1px solid #ddd', 
                                padding: '15px', 
                                borderRadius: '8px',
                                backgroundColor: 'white',
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center'
                            }}>
                                <div>
                                    <h4 style={{ margin: '0 0 5px 0', color: '#2c3e50' }}>
                                        {plant.nickname}
                                    </h4>
                                    {plant.latin_name && (
                                        <p style={{ 
                                            margin: '0', 
                                            color: '#6c757d', 
                                            fontStyle: 'italic',
                                            fontSize: '14px'
                                        }}>
                                            {plant.latin_name}
                                        </p>
                                    )}
                                    <p style={{ 
                                        margin: '5px 0 0 0', 
                                        fontSize: '12px', 
                                        color: '#6c757d' 
                                    }}>
                                        Added: {new Date(plant.created_at).toLocaleDateString()}
                                    </p>
                                </div>
                                <div style={{ display: 'flex', gap: '10px' }}>
                                    <a 
                                        href={`/plant/${plant.id}`}
                                        style={{ 
                                            padding: '6px 12px', 
                                            backgroundColor: '#007bff', 
                                            color: 'white', 
                                            textDecoration: 'none',
                                            borderRadius: '4px',
                                            fontSize: '14px'
                                        }}
                                    >
                                        Chat
                                    </a>
                                    <button 
                                        onClick={() => removePlant(plant.id)}
                                        style={{ 
                                            padding: '6px 12px', 
                                            backgroundColor: '#dc3545', 
                                            color: 'white', 
                                            border: 'none',
                                            borderRadius: '4px',
                                            cursor: 'pointer',
                                            fontSize: '14px'
                                        }}
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default PlantList;
