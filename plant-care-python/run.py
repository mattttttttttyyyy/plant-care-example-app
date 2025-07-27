#!/usr/bin/env python3
"""
Plant Care Application Runner
A simple Flask application for plant care management with AI chat functionality.
"""

import os
import sys
from app import create_app

def main():
    """Main application entry point"""
    print("🌱 Starting Plant Care Application...")
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY not set. Chat functionality will not work.")
        print("   Please set your OpenAI API key in the .env file or environment variables.")
    
    # Create and run the Flask app
    app = create_app()
    
    print("✅ Application created successfully!")
    print("🌐 Server will be available at: http://localhost:5001")
    print("📚 API Documentation:")
    print("   - GET  /api/plants - List all plants")
    print("   - POST /api/plants - Create new plant")
    print("   - GET  /api/plants/<id> - Get specific plant")
    print("   - PUT  /api/plants/<id> - Update plant")
    print("   - DELETE /api/plants/<id> - Delete plant")
    print("   - POST /api/images/upload/<plant_id> - Upload plant image")
    print("   - POST /api/chat/message/<plant_id> - Send message to AI")
    print("   - GET  /api/chat/history/<plant_id> - Get chat history")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

if __name__ == '__main__':
    main() 