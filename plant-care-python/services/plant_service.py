from flask import Blueprint, request, jsonify, current_app
from database.models import db, Plant
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from services.openai_service import OpenAIService

plant_bp = Blueprint('plants', __name__)

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file):
    """Save uploaded file and return the file path"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Ensure upload directory exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        return file_path
    return None

@plant_bp.route('/', methods=['GET'])
def get_all_plants():
    """Get all plants"""
    try:
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@plant_bp.route('/<int:plant_id>', methods=['GET'])
def get_plant(plant_id):
    """Get a specific plant by ID"""
    try:
        plant = Plant.query.get_or_404(plant_id)
        return jsonify(plant.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@plant_bp.route('/', methods=['POST'])
def create_plant():
    """Create a new plant with optional image upload and OpenAI analysis"""
    try:
        # Check if this is a multipart form data request (with image)
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle form data with image
            nickname = request.form.get('nickname')
            latin_name = request.form.get('latin_name', '')
            english_name = request.form.get('english_name', '')
            description = request.form.get('description', '')
            care_instructions = request.form.get('care_instructions', '')
            
            if not nickname:
                return jsonify({'error': 'Nickname is required'}), 400
            
            # Handle image upload
            image_path = None
            plant_data = {}
            
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    image_path = save_uploaded_file(file)
                    
                    if image_path:
                        # Analyze image with OpenAI
                        openai_service = OpenAIService()
                        plant_data = openai_service.analyze_plant_image(image_path)
                        plant_data = openai_service.validate_plant_data(plant_data)
                        
                        # Override with form data if provided
                        if latin_name:
                            plant_data['latin_name'] = latin_name
                        if english_name:
                            plant_data['english_name'] = english_name
                        if description:
                            plant_data['description'] = description
                        if care_instructions:
                            plant_data['care_instructions'] = care_instructions
                    else:
                        return jsonify({'error': 'Invalid image file'}), 400
            
            # Create plant with analyzed data or form data
            plant = Plant(
                nickname=nickname,
                latin_name=plant_data.get('latin_name', latin_name),
                english_name=plant_data.get('english_name', english_name),
                description=plant_data.get('description', description),
                care_instructions=plant_data.get('care_instructions', care_instructions),
                image_path=image_path
            )
            
        else:
            # Handle JSON request (backward compatibility)
            data = request.get_json()
            
            if not data or 'nickname' not in data:
                return jsonify({'error': 'Nickname is required'}), 400
            
            plant = Plant(
                nickname=data['nickname'],
                latin_name=data.get('latin_name', ''),
                english_name=data.get('english_name', ''),
                description=data.get('description', ''),
                care_instructions=data.get('care_instructions', ''),
                image_path=data.get('image_path', '')
            )
        
        db.session.add(plant)
        db.session.commit()
        
        return jsonify(plant.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@plant_bp.route('/<int:plant_id>', methods=['PUT'])
def update_plant(plant_id):
    """Update a plant"""
    try:
        plant = Plant.query.get_or_404(plant_id)
        data = request.get_json()
        
        if 'nickname' in data:
            plant.nickname = data['nickname']
        if 'latin_name' in data:
            plant.latin_name = data['latin_name']
        if 'english_name' in data:
            plant.english_name = data['english_name']
        if 'description' in data:
            plant.description = data['description']
        if 'care_instructions' in data:
            plant.care_instructions = data['care_instructions']
        if 'image_path' in data:
            plant.image_path = data['image_path']
        
        plant.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(plant.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@plant_bp.route('/<int:plant_id>', methods=['DELETE'])
def delete_plant(plant_id):
    """Delete a plant"""
    try:
        plant = Plant.query.get_or_404(plant_id)
        
        # Delete associated image file if it exists
        if plant.image_path and os.path.exists(plant.image_path):
            os.remove(plant.image_path)
        
        db.session.delete(plant)
        db.session.commit()
        
        return jsonify({'message': 'Plant deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@plant_bp.route('/<int:plant_id>/analyze-image', methods=['POST'])
def analyze_plant_image(plant_id):
    """Analyze an uploaded image for an existing plant"""
    try:
        plant = Plant.query.get_or_404(plant_id)
        
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if not file or not file.filename:
            return jsonify({'error': 'No image file selected'}), 400
        
        # Save the uploaded image
        image_path = save_uploaded_file(file)
        if not image_path:
            return jsonify({'error': 'Invalid image file'}), 400
        
        # Analyze image with OpenAI
        openai_service = OpenAIService()
        plant_data = openai_service.analyze_plant_image(image_path)
        plant_data = openai_service.validate_plant_data(plant_data)
        
        # Update plant with analyzed data
        plant.latin_name = plant_data['latin_name']
        plant.english_name = plant_data['english_name']
        plant.description = plant_data['description']
        plant.care_instructions = plant_data['care_instructions']
        plant.image_path = image_path
        plant.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Plant analyzed successfully',
            'plant': plant.to_dict(),
            'analysis': plant_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 