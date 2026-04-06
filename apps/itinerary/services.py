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
        Generate an itinerary using OpenAI API or demo mode if API key not configured.
        
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
        """
        
        # If API key is not configured, use demo mode
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not configured. Using demo itinerary mode.")
            return self._generate_demo_itinerary(
                destination, number_of_days, budget_level, interests
            )
        
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
    
    def _generate_demo_itinerary(
        self,
        destination: str,
        number_of_days: int,
        budget_level: str,
        interests: List[str]
    ) -> Dict:
        """
        Generate a demo itinerary when OpenAI API key is not configured.
        Useful for testing the website without API access.
        
        Args:
            destination: Main destination
            number_of_days: Trip duration
            budget_level: Budget level
            interests: List of interests
        
        Returns:
            Generated demo itinerary
        """
        
        # Calculate realistic budgets based on level
        daily_rates = {
            'low': {'accommodation': 800, 'meals': 600, 'activities': 400, 'transport': 300, 'misc': 200},
            'mid': {'accommodation': 2000, 'meals': 1500, 'activities': 1000, 'transport': 800, 'misc': 700},
            'luxury': {'accommodation': 5000, 'meals': 3000, 'activities': 2500, 'transport': 1500, 'misc': 1000}
        }
        
        rates = daily_rates.get(budget_level, daily_rates['mid'])
        total_budget = (rates['accommodation'] + rates['meals'] + rates['activities'] + rates['transport'] + rates['misc']) * number_of_days
        
        demo_itineraries = {
            'Kathmandu': {
                'title': f'{number_of_days}-Day {destination} Adventure',
                'summary': f'An exciting {number_of_days}-day exploration of {destination} with cultural sites, local experiences, and memorable adventures.',
                'destination': destination,
                'estimated_total_budget_npr': total_budget,
                'budget_breakdown': {
                    'accommodation': rates['accommodation'] * number_of_days,
                    'meals': rates['meals'] * number_of_days,
                    'activities': rates['activities'] * number_of_days,
                    'transport': rates['transport'] * number_of_days,
                    'miscellaneous': rates['misc'] * number_of_days
                },
                'daily_budget_npr': sum(rates.values()),
                'days': [
                    {
                        'day_number': 1,
                        'title': 'Arrival in Kathmandu',
                        'description': 'Rest and acclimatize after arrival',
                        'location': 'Kathmandu',
                        'accommodation': {
                            'name': 'Hotel in Thamel',
                            'type': 'hotel',
                            'estimated_cost_npr': rates['accommodation'],
                            'description': 'Comfortable mid-range hotel'
                        },
                        'activities': [
                            {
                                'time_start': '14:00',
                                'time_end': '17:00',
                                'name': 'Explore Thamel Area',
                                'description': 'Get oriented in the tourist hub, shop and relax',
                                'type': 'sightseeing',
                                'location': 'Thamel',
                                'estimated_cost_npr': rates['activities'] // 3,
                                'importance_level': 'recommended',
                                'tips': 'Many good cafes and restaurants available'
                            }
                        ],
                        'meals_budget_npr': rates['meals'],
                        'transport_budget_npr': rates['transport']
                    },
                    {
                        'day_number': 2,
                        'title': 'Cultural Tour',
                        'description': 'Explore ancient temples and spiritual sites',
                        'location': 'Kathmandu',
                        'accommodation': {
                            'name': 'Hotel in Thamel',
                            'type': 'hotel',
                            'estimated_cost_npr': rates['accommodation'],
                            'description': 'Comfortable mid-range hotel'
                        },
                        'activities': [
                            {
                                'time_start': '06:00',
                                'time_end': '12:00',
                                'name': 'Temple Tour - Swayambhunath & Boudhanath',
                                'description': 'Visit two of Nepal\'s most sacred sites',
                                'type': 'cultural',
                                'location': 'Kathmandu Valley',
                                'estimated_cost_npr': rates['activities'] // 2,
                                'importance_level': 'must',
                                'tips': 'Bring comfortable walking shoes and camera'
                            },
                            {
                                'time_start': '14:00',
                                'time_end': '17:00',
                                'name': 'Pashupatinath Temple',
                                'description': 'Sacred Hindu pilgrimage site',
                                'type': 'spiritual',
                                'location': 'Pashupatinath',
                                'estimated_cost_npr': rates['activities'] // 4,
                                'importance_level': 'recommended',
                                'tips': 'Respect local customs and dress modestly'
                            }
                        ],
                        'meals_budget_npr': rates['meals'],
                        'transport_budget_npr': rates['transport']
                    },
                    {
                        'day_number': 3,
                        'title': 'Local Experiences',
                        'description': 'Interactive cultural workshops',
                        'location': 'Kathmandu',
                        'accommodation': {
                            'name': 'Hotel in Thamel',
                            'type': 'hotel',
                            'estimated_cost_npr': rates['accommodation'],
                            'description': 'Comfortable mid-range hotel'
                        },
                        'activities': [
                            {
                                'time_start': '09:00',
                                'time_end': '12:00',
                                'name': 'Pottery Workshop',
                                'description': 'Learn traditional Nepali pottery making',
                                'type': 'cultural',
                                'location': 'Bhaktapur',
                                'estimated_cost_npr': 1200,
                                'importance_level': 'recommended',
                                'tips': 'Perfect souvenir - bring home your creation'
                            },
                            {
                                'time_start': '13:00',
                                'time_end': '17:00',
                                'name': 'Cooking Class',
                                'description': 'Cook authentic Nepali dishes with a local chef',
                                'type': 'food',
                                'location': 'Kathmandu',
                                'estimated_cost_npr': rates['activities'] // 2,
                                'importance_level': 'recommended',
                                'tips': 'Learn to make dal bhat and momo'
                            }
                        ],
                        'meals_budget_npr': rates['meals'],
                        'transport_budget_npr': rates['transport']
                    },
                ] + [
                    {
                        'day_number': i,
                        'title': f'Exploration Day {i-3}',
                        'description': 'Flexible day for personal exploration',
                        'location': 'Kathmandu',
                        'accommodation': {
                            'name': 'Hotel in Thamel',
                            'type': 'hotel',
                            'estimated_cost_npr': rates['accommodation'],
                            'description': 'Comfortable mid-range hotel'
                        },
                        'activities': [
                            {
                                'time_start': '10:00',
                                'time_end': '16:00',
                                'name': 'Hidden Gems & Local Markets',
                                'description': 'Explore local areas, visit hidden gems',
                                'type': 'sightseeing',
                                'location': 'Kathmandu',
                                'estimated_cost_npr': rates['activities'],
                                'importance_level': 'optional',
                                'tips': 'Ask locals for hidden spots'
                            }
                        ],
                        'meals_budget_npr': rates['meals'],
                        'transport_budget_npr': rates['transport']
                    }
                    for i in range(4, number_of_days + 1)
                ],
                'travel_tips': [
                    'Best time to visit: October-November',
                    'Use local buses for transportation',
                    'Try authentic dhaba restaurants',
                    'Negotiate prices at local markets',
                    'Respect local customs and traditions'
                ]
            },
            'Pokhara': {
                'title': f'{number_of_days}-Day {destination} Getaway',
                'summary': f'A relaxing {number_of_days}-day getaway in {destination} with lake activities, adventure sports, and mountain views.',
                'destination': destination,
                'estimated_total_budget_npr': total_budget,
                'budget_breakdown': {
                    'accommodation': (rates['accommodation'] * 0.8) * number_of_days,
                    'meals': (rates['meals'] * 0.9) * number_of_days,
                    'activities': (rates['activities'] * 1.2) * number_of_days,
                    'transport': (rates['transport'] * 0.7) * number_of_days,
                    'miscellaneous': (rates['misc'] * 0.8) * number_of_days
                },
                'daily_budget_npr': sum(rates.values()),
                'days': [
                    {
                        'day_number': 1,
                        'title': 'Arrival in Pokhara',
                        'description': 'Travel and settle into lakeside hotel',
                        'location': 'Pokhara',
                        'accommodation': {
                            'name': 'Lakeside Hotel',
                            'type': 'hotel',
                            'estimated_cost_npr': rates['accommodation'],
                            'description': 'Hotel with lake views'
                        },
                        'activities': [
                            {
                                'time_start': '17:00',
                                'time_end': '19:00',
                                'name': 'Evening Lakeside Walk',
                                'description': 'Relax and enjoy the sunset',
                                'type': 'relaxation',
                                'location': 'Phewa Lake',
                                'estimated_cost_npr': 0,
                                'importance_level': 'recommended',
                                'tips': '6 hours drive from Kathmandu'
                            }
                        ],
                        'meals_budget_npr': rates['meals'],
                        'transport_budget_npr': rates['transport']
                    },
                    {
                        'day_number': 2,
                        'title': 'Phewa Lake Activities',
                        'description': 'Lake exploration and water activities',
                        'location': 'Pokhara',
                        'accommodation': {
                            'name': 'Lakeside Hotel',
                            'type': 'hotel',
                            'estimated_cost_npr': rates['accommodation'],
                            'description': 'Hotel with lake views'
                        },
                        'activities': [
                            {
                                'time_start': '05:30',
                                'time_end': '07:30',
                                'name': 'Sunrise at Sarangkot',
                                'description': 'Watch sunrise over Phewa Lake',
                                'type': 'sightseeing',
                                'location': 'Sarangkot',
                                'estimated_cost_npr': rates['activities'] // 3,
                                'importance_level': 'must',
                                'tips': 'Bring a camera and warm jacket'
                            },
                            {
                                'time_start': '10:00',
                                'time_end': '14:00',
                                'name': 'Boating & Temple Visit',
                                'description': 'Boat ride on Phewa Lake and visit Barahi Temple',
                                'type': 'cultural',
                                'location': 'Phewa Lake',
                                'estimated_cost_npr': rates['activities'] // 2,
                                'importance_level': 'recommended',
                                'tips': 'Bring sunscreen and hat'
                            }
                        ],
                        'meals_budget_npr': rates['meals'],
                        'transport_budget_npr': rates['transport']
                    },
                ] + [
                    {
                        'day_number': i,
                        'title': f'Adventure Day {i-2}',
                        'description': 'Adventure activities and exploration',
                        'location': 'Pokhara',
                        'accommodation': {
                            'name': 'Lakeside Hotel',
                            'type': 'hotel',
                            'estimated_cost_npr': rates['accommodation'],
                            'description': 'Hotel with lake views'
                        },
                        'activities': [
                            {
                                'time_start': '08:00',
                                'time_end': '15:00',
                                'name': 'Paragliding or Zip-lining',
                                'description': 'Thrilling adventure activities',
                                'type': 'adventure',
                                'location': 'Pokhara',
                                'estimated_cost_npr': rates['activities'],
                                'importance_level': 'optional',
                                'tips': 'Book activities in advance'
                            }
                        ],
                        'meals_budget_npr': rates['meals'],
                        'transport_budget_npr': rates['transport']
                    }
                    for i in range(3, number_of_days + 1)
                ],
                'travel_tips': [
                    'Best for adventure seekers',
                    'Visit in clear seasons for mountain views',
                    'Try local fish curry',
                    'Book activities in advance during peak season'
                ]
            }
        }
        
        # Get demo itinerary or use default
        itinerary_data = demo_itineraries.get(destination, demo_itineraries['Kathmandu'])
        
        # Add note about demo mode
        if budget_level == 'budget':
            itinerary_data['note'] = 'Demo mode: Budget-friendly options'
        elif budget_level == 'luxury':
            itinerary_data['note'] = 'Demo mode: Luxury recommendations'
        else:
            itinerary_data['note'] = 'Demo mode: Mid-range options'
        
        logger.info(f"Generated demo itinerary for {destination}")
        return {
            'success': True,
            'data': itinerary_data,
            'raw_response': json.dumps(itinerary_data)
        }
    
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
