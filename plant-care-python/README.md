# Plant Care Application - Python Edition

A simple, self-contained plant care application with AI chat functionality built with Python Flask and SQLite.

## Features

- 🌱 **Plant Management**: Add, edit, and delete plants
- 📸 **Image Upload**: Upload and store plant images
- 🤖 **AI Chat**: Get plant care advice from OpenAI
- 💬 **Chat History**: Persistent conversation history
- 📊 **Auto-Summarization**: Automatic chat history summarization
- 🗄️ **Self-contained**: SQLite database, no external dependencies

## Quick Start

### 1. Install Dependencies

```bash
cd plant-care-python
pip install -r requirements.txt
```

### 2. Set Up Environment

Copy the example environment file and add your OpenAI API key:

```bash
cp env_example.txt .env
# Edit .env and add your OpenAI API key
```

### 3. Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

### Plants
- `GET /api/plants` - List all plants
- `POST /api/plants` - Create new plant
- `GET /api/plants/<id>` - Get specific plant
- `PUT /api/plants/<id>` - Update plant
- `DELETE /api/plants/<id>` - Delete plant

### Images
- `POST /api/images/upload/<plant_id>` - Upload plant image
- `GET /api/images/<filename>` - Serve image file
- `GET /api/images/plant/<plant_id>` - Get plant's image

### Chat
- `POST /api/chat/message/<plant_id>` - Send message to AI
- `GET /api/chat/history/<plant_id>` - Get chat history

## Database Schema

### Plants Table
- `id` (Primary Key)
- `nickname` (Required)
- `latin_name`
- `image_path`
- `created_at`
- `updated_at`

### Chat History Table
- `id` (Primary Key)
- `plant_id` (Foreign Key)
- `role` (user/assistant)
- `content`
- `timestamp`
- `is_summary`

## Configuration

The application uses the following configuration (in `config.py`):

- **Database**: SQLite (`plant_care.db`)
- **File Upload**: `static/images/` directory
- **Max File Size**: 16MB
- **Allowed Extensions**: PNG, JPG, JPEG, GIF

## Development

### Project Structure
```
plant-care-python/
├── app.py                 # Main Flask application
├── run.py                 # Application runner
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── database/
│   └── models.py         # SQLAlchemy models
├── services/
│   ├── plant_service.py  # Plant management
│   ├── chat_service.py   # OpenAI integration
│   └── image_service.py  # Image handling
└── static/
    └── images/           # Plant images storage
```

### Adding New Features

1. **New Models**: Add to `database/models.py`
2. **New Services**: Create in `services/` directory
3. **New Routes**: Register blueprints in `app.py`

## Deployment

The application is designed to be self-contained and can run on any system with Python 3.8+.

### Production Deployment

1. Set `FLASK_ENV=production` in environment
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set proper `SECRET_KEY`
4. Configure reverse proxy (Nginx) if needed

## Troubleshooting

### Common Issues

1. **OpenAI API Key Not Set**
   - Set `OPENAI_API_KEY` in `.env` file
   - Chat functionality will be disabled without it

2. **Database Errors**
   - Delete `plant_care.db` to reset database
   - Application will recreate tables on startup

3. **Image Upload Issues**
   - Ensure `static/images/` directory exists
   - Check file size (max 16MB)
   - Verify file extension is allowed

## License

This project is open source and available under the MIT License. 