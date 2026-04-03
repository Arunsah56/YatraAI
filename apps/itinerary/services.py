"""
AI Service for OpenAI integration.
Handles intelligent itinerary generation with Nepal-specific data.
"""

import json
import logging
from typing import Dict, List, Optional
from decouple import config
import openai

logger = logging.getLogger(__name__)


class ItineraryAIService:
    """
    Service for generating itineraries using OpenAI API with Nepal-specific data.
    Integrates local data to craft intelligent, contextual travel plans.
    """
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.api_key = config('OPENAI_API_KEY', default='')
        self.model = config('OPENAI_MODEL', default='gpt-4-turbo-preview')
        self.temperature = config('OPENAI_TEMPERATURE', default=0.7, cast=float)
        
        if self.api_key:
            openai.api_key = self.api_key
    
    def build_system_prompt(self) -> str:
        """
        Build the system prompt for itinerary generation.
        Sets the AI's personality and expertise.
        """
        return """You are an expert travel planner specializing in Nepal tourism. 
You have deep knowledge of:
- Nepal's geography, culture, and local customs
- Hidden gems and off-beat destinations
- Budget optimization and local pricing
- Seasonal weather patterns and trekking conditions
- Local transportation options and logistics
- Cultural sensitivities and travel safety

Create detailed, practical itineraries that balance famous attractions with local experiences.
Always prioritize traveler safety, budget realism, and logistical feasibility.
Format responses as valid JSON."""
    
    def build_user_prompt(
        self,
        destination: str,
        number_of_days: int,
        budget_level: str,
        interests: List[str],
        group_size: int,
        travelers_type: str,
        location_data: Dict = None,
        transport_data: List = None,
        tips_data: Dict = None
    ) -> str:
        """
        Build the user prompt with context and local data.
        
        Args:
            destination: Main destination city
            number_of_days: Trip duration
            budget_level: Budget category (low, mid, luxury)
            interests: List of interests (adventure, culture, etc.)
            group_size: Number of travelers
            travelers_type: Type of travelers (solo, couple, family, group)
            location_data: Local location information
            transport_data: Available transport options
            tips_data: Budget tips and seasonal info
        
        Returns:
            Formatted prompt with all context
        """
        
        budget_context = {
            'low': 'budget travelers on a tight budget (NPR 1500-2000 per day per person)',
            'mid': 'mid-range travelers (NPR 2000-5000 per day per person)',
            'luxury': 'luxury travelers seeking comfort and unique experiences (NPR 5000+ per day per person)'
        }
        
        prompt = f"""Create a detailed {number_of_days}-day itinerary for {travelers_type}(s) with {group_size} total travelers to {destination}, Nepal.

Traveler Profile:
- Group Type: {travelers_type}
- Group Size: {group_size}
- Budget Level: {budget_context.get(budget_level, budget_level)}
- Interests: {', '.join(interests)}

Requirements:
1. Provide day-by-day activities with timing (start/end times)
2. Include accommodation suggestions with estimated costs
3. Calculate daily and total trip budget in NPR
4. Incorporate local experiences and hidden gems
5. Include practical travel tips (what to bring, local customs, safety)
6. Suggest local food experiences
7. Provide transport recommendations with estimated costs

Nepal Context:
- Main Language: Nepali (English widely spoken in tourist areas)
- Currency: Nepali Rupee (NPR) 
- Timezone: UTC+5:45
- Travel Season: October-November and March-May are best
- Trekking Season: September-November and March-May

Budget Reference (NPR per person):
- Budget Guesthouse: NPR 500-1000/night
- Mid-range Hotel: NPR 1500-3000/night
- Mid-range Meal: NPR 300-500
- Activities/Entry Fees: NPR 100-1000
- Transport (Local): NPR 20-500 depending on distance

"""
        
        if location_data:
            prompt += f"\nLocation Context:\n{json.dumps(location_data, indent=2)}\n"
        
        if transport_data:
            prompt += f"\nTransport Options:\n{json.dumps(transport_data[:5], indent=2)}\n"
        
        if tips_data:
            prompt += f"\nLocal Tips & Seasonal Info:\n{json.dumps(tips_data, indent=2)}\n"
        
        prompt += """

Provide the response ONLY as a valid JSON object with this structure:
{
    "title": "Itinerary Title",
    "summary": "Brief overview",
    "estimated_total_budget_npr": <number>,
    "budget_breakdown": {
        "accommodation": <number>,
        "meals": <number>,
        "transport": <number>,
        "activities": <number>,
        "miscellaneous": <number>
    },
    "daily_budget_npr": <number>,
    "days": [
        {
            "day_number": 1,
            "title": "Day Title",
            "description": "Day overview",
            "location": "City/Area",
            "accommodation": {
                "name": "Hotel/Guesthouse name",
                "type": "hotel|guesthouse|homestay|lodge|camping",
                "estimated_cost_npr": <number>,
                "description": "Brief description"
            },
            "activities": [
                {
                    "time_start": "08:00",
                    "time_end": "12:00",
                    "name": "Activity Name",
                    "description": "What to do",
                    "type": "sightseeing|trekking|adventure|cultural|food|relaxation|spiritual|shopping|nightlife",
                    "location": "Specific location",
                    "estimated_cost_npr": <number>,
                    "importance_level": "must|recommended|optional",
                    "tips": "Local tips"
                }
            ],
            "meals": [
                {
                    "type": "breakfast|lunch|dinner",
                    "suggestion": "What to eat",
                    "estimated_cost_npr": <number>
                }
            ],
            "day_budget_npr": <number>,
            "travel_notes": "Logistics and tips",
            "packing_tips": "What to bring for this day"
        }
    ],
    "travel_tips": [
        "Important tips for the entire trip"
    ],
    "safety_notes": "Safety recommendations",
    "cultural_notes": "Cultural sensitivities",
    "emergency_contacts": {
        "police": "100",
        "ambulance": "100",
        "tourist_police": "+977-1-4247041"
    }
}

Ensure all costs are realistic and in NPR. Make the itinerary practical and safe for the travelers."""
        
        return prompt
    
    def generate_itinerary(
        self,
        destination: str,
        number_of_days: int,
        budget_level: str,
        interests: List[str],
        group_size: int = 1,
        travelers_type: str = 'solo',
        location_data: Dict = None,
        transport_data: List = None,
        tips_data: Dict = None
    ) -> Dict:
        """
        Generate an itinerary using OpenAI API.
        
        Args:
            destination: Main destination
            number_of_days: Trip duration
            budget_level: Budget level
            interests: List of traveler interests
            group_size: Number of travelers
            travelers_type: Type of travelers
            location_data: Local location info
            transport_data: Transport options
            tips_data: Tips and seasonal data
        
        Returns:
            Generated itinerary as dictionary
        
        Raises:
            Exception: If API call fails or response is invalid
        """
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        
        try:
            system_prompt = self.build_system_prompt()
            user_prompt = self.build_user_prompt(
                destination=destination,
                number_of_days=number_of_days,
                budget_level=budget_level,
                interests=interests,
                group_size=group_size,
                travelers_type=travelers_type,
                location_data=location_data,
                transport_data=transport_data,
                tips_data=tips_data
            )
            
            logger.info(f"Calling OpenAI API for itinerary: {destination}, {number_of_days} days")
            
            message = openai.ChatCompletion.create(
                model=self.model,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            response_text = message['choices'][0]['message']['content']
            
            # Parse JSON response
            try:
                itinerary_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    itinerary_data = json.loads(json_match.group())
                else:
                    logger.error("Failed to parse AI response as JSON")
                    raise ValueError("Invalid response format from AI")
            
            logger.info(f"Successfully generated itinerary for {destination}")
            return {
                'success': True,
                'data': itinerary_data,
                'raw_response': response_text
            }
        
        except openai.error.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"AI service error: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating itinerary: {str(e)}")
            raise
    
    def validate_itinerary_structure(self, itinerary_data: Dict) -> bool:
        """
        Validate that generated itinerary has required fields.
        
        Args:
            itinerary_data: Generated itinerary dictionary
        
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['title', 'estimated_total_budget_npr', 'days']
        return all(field in itinerary_data for field in required_fields)
