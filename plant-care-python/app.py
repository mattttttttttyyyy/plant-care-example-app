from flask import Flask, jsonify, request
from flask_cors import CORS
from database.models import db, Plant, ChatHistory
from config import config
import os

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Import and register blueprints
    from services.plant_service import plant_bp
    from services.chat_service import chat_bp
    from services.image_service import image_bp
    
    app.register_blueprint(plant_bp, url_prefix='/api/plants')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(image_bp, url_prefix='/api/images')
    
    @app.route('/')
    def index():
        return jsonify({'message': 'Plant Care API is running!'})
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'database': 'connected'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001) 