from flask import Blueprint, request, jsonify, current_app
from database.models import db, Plant, ChatHistory
from openai import OpenAI
import base64
import os
from datetime import datetime

chat_bp = Blueprint('chat', __name__)

def get_openai_client():
    api_key = current_app.config.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not configured")
    return OpenAI(api_key=api_key)

def create_system_prompt(plant):
    return f"""You are a helpful AI assistant specializing in plant care. You will provide advice based on the user's questions and the history of their plant.

The plant's nickname is {plant.nickname} and its latin name is {plant.latin_name or 'Unknown'}.

You should provide helpful, accurate plant care advice. Be specific about watering, light, soil, and other care requirements. If you're not sure about something, say so rather than guessing."""

def get_chat_history(plant_id, limit=10):
    return ChatHistory.query.filter_by(plant_id=plant_id).order_by(ChatHistory.timestamp.desc()).limit(limit).all()

def should_summarize(plant_id):
    non_summary_count = ChatHistory.query.filter_by(
        plant_id=plant_id,
        is_summary=False
    ).count()
    return non_summary_count >= 10

def create_summary_prompt(messages):
    conversation = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])
    return f"Summarize the following conversation about a plant care: {conversation}"

def summarize_chat_history(plant_id):
    try:
        recent_messages = ChatHistory.query.filter_by(
            plant_id=plant_id,
            is_summary=False
        ).order_by(ChatHistory.timestamp.desc()).limit(10).all()

        if len(recent_messages) < 5:
            return

        client = get_openai_client()
        summary_prompt = create_summary_prompt(recent_messages)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes plant care conversations."},
                {"role": "user", "content": summary_prompt}
            ],
            max_tokens=200
        )

        summary_content = response.choices[0].message.content

        summary = ChatHistory(
            plant_id=plant_id,
            role='assistant',
            content=summary_content,
            is_summary=True
        )

        db.session.add(summary)
        db.session.commit()

        for msg in recent_messages:
            msg.is_summary = True
        db.session.commit()

    except Exception as e:
        print(f"Error summarizing chat history: {e}")
        db.session.rollback()

@chat_bp.route('/message/<int:plant_id>', methods=['POST'])
def send_message(plant_id):
    try:
        plant = Plant.query.get_or_404(plant_id)

        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400

        user_message = data['message']
        image_data = data.get('image')

        user_chat = ChatHistory(
            plant_id=plant_id,
            role='user',
            content=user_message
        )
        db.session.add(user_chat)
        db.session.commit()

        client = get_openai_client()
        
        # Prepare the content for the API
        content = []
        
        # Add text content
        content.append({
            "type": "text",
            "text": user_message
        })
        
        # Add image content if provided
        if image_data:
            try:
                # Remove data URL prefix if present
                if image_data.startswith('data:image/'):
                    image_data = image_data.split(',')[1]
                
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                })
            except Exception as e:
                print(f"Error processing image: {e}")

        # Create the API request
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": create_system_prompt(plant)
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=500
        )

        ai_response = response.choices[0].message.content

        ai_chat = ChatHistory(
            plant_id=plant_id,
            role='assistant',
            content=ai_response
        )
        db.session.add(ai_chat)
        db.session.commit()

        if should_summarize(plant_id):
            summarize_chat_history(plant_id)

        return jsonify({
            'response': ai_response,
            'plant_id': plant_id
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error in send_message: {e}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/history/<int:plant_id>', methods=['GET'])
def get_chat_history(plant_id):
    try:
        plant = Plant.query.get_or_404(plant_id)
        history = ChatHistory.query.filter_by(plant_id=plant_id).order_by(ChatHistory.timestamp.asc()).all()
        return jsonify([msg.to_dict() for msg in history]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 