import os
import base64
import json
from openai import OpenAI
from flask import current_app

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])
    
    def analyze_plant_image(self, image_path):
        """
        Analyze a plant image using OpenAI Vision API and return structured plant data
        """
        try:
            # Read and encode the image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Prepare the prompt for plant identification
            prompt = """
            Analyze this plant image and provide the following information in JSON format:
            {
                "latin_name": "The scientific/Latin name of the plant",
                "english_name": "The common English name of the plant",
                "description": "A detailed description of the plant's appearance, characteristics, and features",
                "care_instructions": "Comprehensive care instructions including watering, light requirements, soil type, temperature, humidity, and any special care needs"
            }
            
            Please be as accurate as possible with the plant identification and provide detailed, practical care instructions.
            """
            
            # Call OpenAI Vision API
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            # Extract and parse the JSON response
            content = response.choices[0].message.content
            plant_data = json.loads(content)
            
            return plant_data
            
        except Exception as e:
            # Return default structure if analysis fails
            return {
                "latin_name": "",
                "english_name": "",
                "description": f"Unable to analyze image: {str(e)}",
                "care_instructions": "Please provide care instructions manually."
            }
    
    def validate_plant_data(self, plant_data):
        """
        Validate that the plant data contains all required fields
        """
        required_fields = ['latin_name', 'english_name', 'description', 'care_instructions']
        for field in required_fields:
            if field not in plant_data:
                plant_data[field] = ""
        return plant_data 