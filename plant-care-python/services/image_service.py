from flask import Blueprint, request, jsonify, send_from_directory, current_app
from database.models import db, Plant
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

image_bp = Blueprint('images', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_filename(original_filename):
    """Generate unique filename"""
    ext = original_filename.rsplit('.', 1)[1].lower()
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{ext}"

@image_bp.route('/upload/<int:plant_id>', methods=['POST'])
def upload_image(plant_id):
    """Upload image for a specific plant"""
    try:
        # Check if plant exists
        plant = Plant.query.get_or_404(plant_id)
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Generate unique filename
        filename = generate_filename(file.filename)
        
        # Save file
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Update plant with image path
        plant.image_path = filename
        plant.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Image uploaded successfully',
            'filename': filename,
            'plant_id': plant_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@image_bp.route('/<filename>', methods=['GET'])
def get_image(filename):
    """Serve image file"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        return send_from_directory(upload_folder, filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@image_bp.route('/plant/<int:plant_id>', methods=['GET'])
def get_plant_image(plant_id):
    """Get image for a specific plant"""
    try:
        plant = Plant.query.get_or_404(plant_id)
        
        if not plant.image_path:
            return jsonify({'error': 'No image found for this plant'}), 404
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        return send_from_directory(upload_folder, plant.image_path)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 