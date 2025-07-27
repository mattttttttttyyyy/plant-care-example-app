import os
import base64
import json
from openai import OpenAI
from flask import current_app

class OpenAIService:
    def __init__(self):
        api_key = current_app.config.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not configured. Please set it in your environment variables.")
        self.client = OpenAI(api_key=api_key)
    
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
            You are a plant identification expert. Analyze this plant image and provide the following information in JSON format:
            {
                "latin_name": "The scientific/Latin name of the plant (e.g., Monstera deliciosa, Ficus lyrata, Philodendron hederaceum). If you cannot identify the specific species, provide the genus name followed by 'sp.' (e.g., Monstera sp.).",
                "english_name": "The common English name of the plant (e.g., Swiss Cheese Plant, Fiddle Leaf Fig, Heartleaf Philodendron). If you cannot identify the specific species, provide a general description like 'Large-leafed tropical plant'.",
                "description": "A detailed description of the plant's appearance, characteristics, and features including leaf shape, color, size, and any distinctive markings.",
                "care_instructions": {
                    "watering": "Specific watering instructions including frequency and method",
                    "light_requirements": "Light needs including intensity and duration",
                    "soil_type": "Recommended soil type and composition",
                    "temperature": "Optimal temperature range and tolerance",
                    "humidity": "Humidity requirements and recommendations",
                    "special_care_needs": "Any special care requirements, pruning, repotting, or other maintenance needs"
                }
            }
            
            IMPORTANT: 
            - Focus on identifying the plant species first, then provide care instructions
            - If you cannot identify the exact species, provide the best possible identification
            - For common houseplants, try to identify the specific species
            - Provide detailed, practical care instructions based on the plant type
            - Be specific about watering, light, and other care requirements
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
            content = response.choices[0].message.content.strip()
            
            if not content:
                raise ValueError("OpenAI returned an empty response")
            
            # Try to parse the JSON response
            try:
                plant_data = json.loads(content)
            except json.JSONDecodeError as e:
                # If JSON parsing fails, try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    plant_data = json.loads(json_match.group())
                else:
                    raise ValueError(f"Could not parse JSON from OpenAI response: {content[:200]}")
            
            return plant_data
            
        except Exception as e:
            error_msg = str(e)
            if "OPENAI_API_KEY" in error_msg:
                return {
                    "latin_name": "",
                    "english_name": "",
                    "description": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.",
                    "care_instructions": "Please provide care instructions manually."
                }
            elif "rate limit" in error_msg.lower():
                return {
                    "latin_name": "",
                    "english_name": "",
                    "description": "OpenAI rate limit exceeded. Please try again later.",
                    "care_instructions": "Please provide care instructions manually."
                }
            else:
                return {
                    "latin_name": "",
                    "english_name": "",
                    "description": f"Unable to analyze image: {error_msg}",
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