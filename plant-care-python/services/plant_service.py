from flask import Blueprint, request, jsonify, current_app
from database.models import db, Plant
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

plant_bp = Blueprint('plants', __name__)

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def format_care_instructions(care_instructions):
    """Convert care instructions dictionary to formatted string"""
    if isinstance(care_instructions, dict):
        formatted = []
        for key, value in care_instructions.items():
            # Convert key from snake_case to Title Case
            title = key.replace('_', ' ').title()
            formatted.append(f"{title}: {value}")
        return "\n".join(formatted)
    elif isinstance(care_instructions, str):
        return care_instructions
    else:
        return str(care_instructions)

def generate_filename(original_filename):
    """Generate unique filename"""
    ext = original_filename.rsplit('.', 1)[1].lower()
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{ext}"

def get_openai_service():
    """Get OpenAI service with proper error handling"""
    try:
        from services.openai_service import OpenAIService
        return OpenAIService()
    except Exception as e:
        # Return None if OpenAI service can't be initialized (e.g., missing API key, import errors, etc.)
        print(f"OpenAI service initialization failed: {str(e)}")
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
        print(f"Content-Type: {request.content_type}")
        print(f"Request method: {request.method}")
        print(f"Request files: {list(request.files.keys()) if request.files else 'No files'}")
        
        # Check if this is a multipart form data request (with image)
        if request.content_type and 'multipart/form-data' in request.content_type:
            print("Processing multipart form data request")
            
            # Handle form data with image
            nickname = request.form.get('nickname')
            latin_name = request.form.get('latin_name', '')
            english_name = request.form.get('english_name', '')
            description = request.form.get('description', '')
            care_instructions = request.form.get('care_instructions', '')
            
            print(f"Form data - nickname: {nickname}, latin_name: {latin_name}")
            
            if not nickname:
                return jsonify({'error': 'Nickname is required'}), 400
            
            # Handle image upload
            image_path = None
            plant_data = {}
            
            if 'image' in request.files:
                print("Image file found in request")
                file = request.files['image']
                if file and file.filename:
                    print(f"Processing image file: {file.filename}")
                    
                    try:
                        # Check if file type is allowed
                        if not allowed_file(file.filename):
                            return jsonify({'error': 'File type not allowed'}), 400
                        
                        # Generate unique filename
                        filename = generate_filename(file.filename)
                        print(f"Generated filename: {filename}")
                        
                        # Save file
                        upload_folder = current_app.config['UPLOAD_FOLDER']
                        os.makedirs(upload_folder, exist_ok=True)
                        file_path = os.path.join(upload_folder, filename)
                        file.save(file_path)
                        print(f"File saved to: {file_path}")
                        
                        image_path = filename
                        
                        # Try to analyze image with OpenAI
                        print("Attempting OpenAI analysis...")
                        openai_service = get_openai_service()
                        if openai_service:
                            try:
                                plant_data = openai_service.analyze_plant_image(file_path)
                                print(f"OpenAI analysis result: {plant_data}")
                                plant_data = openai_service.validate_plant_data(plant_data)
                            except Exception as e:
                                print(f"OpenAI analysis failed: {str(e)}")
                                plant_data = {
                                    "latin_name": "",
                                    "english_name": "",
                                    "description": f"Image analysis failed: {str(e)}",
                                    "care_instructions": "Please provide care instructions manually."
                                }
                        else:
                            print("OpenAI service not available")
                            # OpenAI service not available
                            plant_data = {
                                "latin_name": "",
                                "english_name": "",
                                "description": "OpenAI API key not configured. Image analysis disabled.",
                                "care_instructions": "Please provide care instructions manually."
                            }
                        
                        # Override with form data if provided
                        if latin_name:
                            plant_data['latin_name'] = latin_name
                        if english_name:
                            plant_data['english_name'] = english_name
                        if description:
                            plant_data['description'] = description
                        if care_instructions:
                            plant_data['care_instructions'] = care_instructions
                            
                    except Exception as e:
                        print(f"Image processing failed: {str(e)}")
                        return jsonify({'error': f'Image processing failed: {str(e)}'}), 500
                else:
                    print("No valid image file found")
            else:
                print("No image file in request")
            
            # Create plant with analyzed data or form data
            print(f"Creating plant with data: {plant_data}")
            
            # Format care instructions if it's a dictionary
            formatted_care_instructions = format_care_instructions(plant_data.get('care_instructions', care_instructions))
            print(f"Formatted care instructions: {formatted_care_instructions}")
            
            plant = Plant(
                nickname=nickname,
                latin_name=plant_data.get('latin_name', latin_name),
                english_name=plant_data.get('english_name', english_name),
                description=plant_data.get('description', description),
                care_instructions=formatted_care_instructions,
                image_path=image_path
            )
            
        else:
            print("Processing JSON request")
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
        
        print("Adding plant to database...")
        db.session.add(plant)
        db.session.commit()
        print(f"Plant created successfully with ID: {plant.id}")
        
        return jsonify(plant.to_dict()), 201
        
    except Exception as e:
        print(f"Error in create_plant: {str(e)}")
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
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid image file'}), 400
        
        filename = generate_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Try to analyze image with OpenAI
        openai_service = get_openai_service()
        if openai_service:
            plant_data = openai_service.analyze_plant_image(file_path)
            plant_data = openai_service.validate_plant_data(plant_data)
        else:
            # OpenAI service not available
            plant_data = {
                "latin_name": "",
                "english_name": "",
                "description": "OpenAI API key not configured. Image analysis disabled.",
                "care_instructions": "Please provide care instructions manually."
            }
        
        # Update plant with analyzed data
        plant.latin_name = plant_data['latin_name']
        plant.english_name = plant_data['english_name']
        plant.description = plant_data['description']
        plant.care_instructions = format_care_instructions(plant_data['care_instructions'])
        plant.image_path = filename
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