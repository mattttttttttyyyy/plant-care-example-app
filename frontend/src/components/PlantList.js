import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PlantList = () => {
    const [plants, setPlants] = useState([]);
    const [newPlant, setNewPlant] = useState({ 
        nickname: '', 
        latin_name: '', 
        english_name: '', 
        description: '', 
        care_instructions: '' 
    });
    const [selectedImage, setSelectedImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isAddingPlant, setIsAddingPlant] = useState(false);

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
            
            setSelectedImage(file);
            
            // Create preview
            const reader = new FileReader();
            reader.onload = (e) => {
                setImagePreview(e.target.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const clearImage = () => {
        setSelectedImage(null);
        setImagePreview(null);
    };

    const addPlant = async () => {
        if (!newPlant.nickname.trim()) {
            alert('Please enter a plant nickname');
            return;
        }

        setIsAddingPlant(true);
        setError(null);

        try {
            let response;
            
            if (selectedImage) {
                // Use FormData for multipart upload with image
                const formData = new FormData();
                formData.append('nickname', newPlant.nickname);
                formData.append('latin_name', newPlant.latin_name);
                formData.append('english_name', newPlant.english_name);
                formData.append('description', newPlant.description);
                formData.append('care_instructions', newPlant.care_instructions);
                formData.append('image', selectedImage);
                
                response = await axios.post('/api/plants', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
            } else {
                // Use JSON for text-only data
                response = await axios.post('/api/plants', newPlant);
            }
            
            setPlants([...plants, response.data]);
            setNewPlant({ 
                nickname: '', 
                latin_name: '', 
                english_name: '', 
                description: '', 
                care_instructions: '' 
            });
            clearImage();
            setError(null);
        } catch (error) {
            console.error('Error adding plant:', error);
            setError('Failed to add plant: ' + (error.response?.data?.error || error.message));
        } finally {
            setIsAddingPlant(false);
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
        <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
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
                
                {/* Image Upload Section */}
                <div style={{ marginBottom: '20px' }}>
                    <label style={{ 
                        display: 'block', 
                        marginBottom: '10px', 
                        fontWeight: 'bold',
                        color: '#495057'
                    }}>
                        Plant Image (Optional - AI will analyze and identify your plant)
                    </label>
                    <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                        <input
                            type="file"
                            onChange={handleImageChange}
                            accept="image/*"
                            style={{ display: 'none' }}
                            id="plant-image-input"
                        />
                        <label htmlFor="plant-image-input" style={{ 
                            padding: '10px 16px', 
                            backgroundColor: '#007bff', 
                            color: 'white', 
                            borderRadius: '4px',
                            cursor: 'pointer',
                            display: 'inline-block'
                        }}>
                            📷 Choose Image
                        </label>
                        {selectedImage && (
                            <button 
                                onClick={clearImage}
                                style={{ 
                                    padding: '8px 12px', 
                                    backgroundColor: '#6c757d', 
                                    color: 'white', 
                                    border: 'none',
                                    borderRadius: '4px',
                                    cursor: 'pointer'
                                }}
                            >
                                Clear
                            </button>
                        )}
                    </div>
                    {imagePreview && (
                        <div style={{ marginTop: '10px' }}>
                            <img 
                                src={imagePreview} 
                                alt="Preview" 
                                style={{ 
                                    maxWidth: '200px', 
                                    maxHeight: '200px', 
                                    borderRadius: '4px',
                                    border: '1px solid #ddd'
                                }}
                            />
                            <p style={{ margin: '5px 0 0 0', fontSize: '12px', color: '#6c757d' }}>
                                {selectedImage?.name}
                            </p>
                        </div>
                    )}
                </div>

                {/* Plant Information Form */}
                <div style={{ display: 'grid', gap: '15px' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                        <input
                            type="text"
                            placeholder="Plant nickname *"
                            value={newPlant.nickname}
                            onChange={e => setNewPlant({ ...newPlant, nickname: e.target.value })}
                            onKeyPress={handleKeyPress}
                            style={{ 
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
                                padding: '8px', 
                                border: '1px solid #ddd',
                                borderRadius: '4px'
                            }}
                        />
                    </div>
                    
                    <input
                        type="text"
                        placeholder="English name (optional)"
                        value={newPlant.english_name}
                        onChange={e => setNewPlant({ ...newPlant, english_name: e.target.value })}
                        onKeyPress={handleKeyPress}
                        style={{ 
                            padding: '8px', 
                            border: '1px solid #ddd',
                            borderRadius: '4px'
                        }}
                    />
                    
                    <textarea
                        placeholder="Description (optional)"
                        value={newPlant.description}
                        onChange={e => setNewPlant({ ...newPlant, description: e.target.value })}
                        rows="3"
                        style={{ 
                            padding: '8px', 
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            resize: 'vertical'
                        }}
                    />
                    
                    <textarea
                        placeholder="Care instructions (optional)"
                        value={newPlant.care_instructions}
                        onChange={e => setNewPlant({ ...newPlant, care_instructions: e.target.value })}
                        rows="3"
                        style={{ 
                            padding: '8px', 
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            resize: 'vertical'
                        }}
                    />
                    
                    <button 
                        onClick={addPlant}
                        disabled={!newPlant.nickname.trim() || isAddingPlant}
                        style={{ 
                            padding: '12px 16px', 
                            backgroundColor: newPlant.nickname.trim() && !isAddingPlant ? '#28a745' : '#6c757d', 
                            color: 'white', 
                            border: 'none',
                            borderRadius: '4px',
                            cursor: newPlant.nickname.trim() && !isAddingPlant ? 'pointer' : 'not-allowed',
                            fontSize: '16px'
                        }}
                    >
                        {isAddingPlant ? 'Adding Plant...' : 'Add Plant'}
                    </button>
                </div>
                
                <div style={{ 
                    marginTop: '15px', 
                    padding: '10px', 
                    backgroundColor: '#e7f3ff', 
                    borderRadius: '4px',
                    fontSize: '14px',
                    color: '#0056b3'
                }}>
                    💡 <strong>Tip:</strong> Upload an image of your plant and AI will automatically identify it and fill in the details for you!
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
                    <div style={{ display: 'grid', gap: '20px' }}>
                        {plants.map(plant => (
                            <div key={plant.id} style={{ 
                                border: '1px solid #ddd', 
                                padding: '20px', 
                                borderRadius: '8px',
                                backgroundColor: 'white',
                                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                            }}>
                                <div style={{ display: 'flex', gap: '20px' }}>
                                    {/* Plant Image */}
                                    {plant.image_path && (
                                        <div style={{ flexShrink: 0 }}>
                                            <img 
                                                src={`/api/images/${plant.image_path}`} 
                                                alt={plant.nickname}
                                                style={{ 
                                                    width: '120px', 
                                                    height: '120px', 
                                                    objectFit: 'cover',
                                                    borderRadius: '8px',
                                                    border: '1px solid #eee'
                                                }}
                                            />
                                        </div>
                                    )}
                                    
                                    {/* Plant Information */}
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                                            <div>
                                                <h4 style={{ margin: '0 0 5px 0', color: '#2c3e50', fontSize: '18px' }}>
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
                                                        margin: '0 0 5px 0', 
                                                        color: '#495057',
                                                        fontSize: '14px'
                                                    }}>
                                                        {plant.english_name}
                                                    </p>
                                                )}
                                            </div>
                                            <div style={{ display: 'flex', gap: '10px' }}>
                                                <a 
                                                    href={`/plant/${plant.id}`}
                                                    style={{ 
                                                        padding: '8px 16px', 
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
                                                        padding: '8px 16px', 
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
                                        
                                        {/* Plant Description */}
                                        {plant.description && (
                                            <div style={{ marginBottom: '10px' }}>
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
                                            <div style={{ 
                                                backgroundColor: '#f8f9fa', 
                                                padding: '10px', 
                                                borderRadius: '4px',
                                                marginBottom: '10px'
                                            }}>
                                                <strong style={{ color: '#495057', fontSize: '14px' }}>Care Instructions:</strong>
                                                <p style={{ 
                                                    margin: '5px 0 0 0', 
                                                    color: '#495057',
                                                    fontSize: '14px',
                                                    lineHeight: '1.4'
                                                }}>
                                                    {plant.care_instructions}
                                                </p>
                                            </div>
                                        )}
                                        
                                        <p style={{ 
                                            margin: '10px 0 0 0', 
                                            fontSize: '12px', 
                                            color: '#6c757d' 
                                        }}>
                                            Added: {new Date(plant.created_at).toLocaleDateString()}
                                        </p>
                                    </div>
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
