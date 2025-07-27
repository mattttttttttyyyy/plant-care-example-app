from flask import Blueprint, request, jsonify
from database.models import db, Plant
from datetime import datetime

plant_bp = Blueprint('plants', __name__)

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
    """Create a new plant"""
    try:
        data = request.get_json()
        
        if not data or 'nickname' not in data:
            return jsonify({'error': 'Nickname is required'}), 400
        
        plant = Plant(
            nickname=data['nickname'],
            latin_name=data.get('latin_name', ''),
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
        db.session.delete(plant)
        db.session.commit()
        
        return jsonify({'message': 'Plant deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 