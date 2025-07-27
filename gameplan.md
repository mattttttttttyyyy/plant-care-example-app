# Plant Care App - Python Implementation Game Plan

## **Overview**
Transform the existing Java/Spring Boot application into a simple Python server with SQLite database, keeping everything self-contained for local deployment.

## **Phase 1: Python Backend Core Setup**

### **Step 1: Project Structure Setup**
```
plant-care/
├── app.py                 # Main Flask application
├── database/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   └── database.py        # Database initialization
├── services/
│   ├── __init__.py
│   ├── plant_service.py   # Plant business logic
│   ├── chat_service.py    # OpenAI integration
│   └── image_service.py   # Image handling
├── static/
│   ├── images/            # Plant images storage
│   └── uploads/           # Upload directory
├── templates/             # HTML templates (if needed)
├── requirements.txt       # Python dependencies
└── config.py             # Configuration settings
```

### **Step 2: Dependencies Setup**
**File:** `requirements.txt`
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-CORS==4.0.0
openai==1.3.0
Pillow==10.1.0
python-dotenv==1.0.0
```

### **Step 3: Database Models**
**File:** `database/models.py`
- **Plant Model:** id, nickname, latin_name, created_at, updated_at, image_path
- **ChatHistory Model:** id, plant_id, role, content, timestamp, is_summary
- **SQLite Database:** Self-contained, no external database needed

### **Step 4: Flask Application Setup**
**File:** `app.py`
- Flask app with SQLAlchemy integration
- CORS configuration for frontend
- Database initialization
- Basic routing structure

## **Phase 2: Plant Management API**

### **Step 5: Plant Service**
**File:** `services/plant_service.py`
- CRUD operations for plants
- SQLite database operations
- Image path management

### **Step 6: Plant API Endpoints**
**File:** `app.py` (plant routes)
- `GET /api/plants` - List all plants
- `POST /api/plants` - Create new plant
- `GET /api/plants/<id>` - Get specific plant
- `PUT /api/plants/<id>` - Update plant
- `DELETE /api/plants/<id>` - Delete plant

## **Phase 3: Image Handling**

### **Step 7: Image Service**
**File:** `services/image_service.py`
- Local file storage in `static/images/`
- Image upload handling
- File naming and organization
- Image serving endpoints

### **Step 8: Image API Endpoints**
- `POST /api/images/upload/<plant_id>` - Upload plant image
- `GET /api/images/<filename>` - Serve image file

## **Phase 4: OpenAI Chat Integration**

### **Step 9: Chat Service**
**File:** `services/chat_service.py`
- OpenAI API integration
- Chat history management
- Message summarization (every 10 messages)
- Context-aware prompts

### **Step 10: Chat API Endpoints**
- `POST /api/chat/message/<plant_id>` - Send message to AI
- `GET /api/chat/history/<plant_id>` - Get chat history

## **Phase 5: Frontend Integration**

### **Step 11: Frontend Setup**
- Keep existing React frontend in `frontend/` directory
- Update API calls to point to Python backend
- Configure proxy to `http://localhost:5000` (Flask default)

### **Step 12: API Integration**
- Update all fetch calls to use new Python endpoints
- Handle image uploads with FormData
- Implement error handling for Python backend

## **Phase 6: Configuration & Deployment**

### **Step 13: Environment Setup**
**File:** `config.py`
- Database configuration (SQLite)
- OpenAI API key management
- File upload settings
- Development/production modes

### **Step 14: Startup Scripts**
- `run.py` - Main application runner
- Database initialization script
- Environment setup instructions

## **Key Differences from Java Version:**

1. **Database:** SQLite instead of PostgreSQL (self-contained)
2. **Framework:** Flask instead of Spring Boot (lighter weight)
3. **Dependencies:** Minimal Python packages vs Maven dependencies
4. **Deployment:** Single Python process vs JVM
5. **Configuration:** Simple config.py vs application.properties
6. **File Storage:** Local filesystem instead of complex storage service

## **Implementation Priority:**

1. **Core Setup** (Steps 1-4) - Basic Flask app with SQLite
2. **Plant Management** (Steps 5-6) - CRUD operations
3. **Image Handling** (Steps 7-8) - File uploads
4. **Chat Integration** (Steps 9-10) - OpenAI functionality
5. **Frontend Updates** (Steps 11-12) - React integration
6. **Polish** (Steps 13-14) - Configuration and deployment

## **Benefits of Python Implementation:**

- **Self-contained:** No external database or services needed
- **Lightweight:** Minimal dependencies and resource usage
- **Simple deployment:** Single Python file to run
- **Easy development:** Python's simplicity vs Java complexity
- **Cross-platform:** Works on any OS with Python installed

Would you like me to start implementing any specific phase or component?