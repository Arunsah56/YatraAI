"""
Management command to populate the database with comprehensive sample data.
Includes locations, hidden gems, local experiences, seasonal tips, and budget tips.
"""

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from apps.locations.models import Location, HiddenGem
from apps.tips.models import LocalExperience, SeasonalTip, BudgetTip


class Command(BaseCommand):
    help = 'Populate database with sample locations and hidden gems'

    def handle(self, *args, **options):
        # Clear existing data
        HiddenGem.objects.all().delete()
        Location.objects.all().delete()

        # Create sample locations
        locations_data = [
            {
                'name': 'Kathmandu',
                'region': 'kathmandu',
                'description': 'The capital of Nepal and the heart of the Kathmandu Valley.',
                'altitude': 'mid',
                'latitude': 27.7172,
                'longitude': 85.3240,
                'best_time_visit': 'October-November',
                'weather_info': 'Clear skies, pleasant temperature',
                'distance_from_kathmandu_km': 0,
                'travel_time_hours': 0,
                'primary_attraction': 'Swayambhunath Stupa',
                'emoji': '🏛️',
                'popularity_score': 10,
            },
            {
                'name': 'Pokhara',
                'region': 'central',
                'description': 'A beautiful lakeside city known for scenic views and adventure activities.',
                'altitude': 'mid',
                'latitude': 28.2096,
                'longitude': 83.9856,
                'best_time_visit': 'September-November',
                'weather_info': 'Cool and clear',
                'distance_from_kathmandu_km': 200,
                'travel_time_hours': 6,
                'primary_attraction': 'Phewa Lake',
                'emoji': '🏞️',
                'popularity_score': 9,
            },
            {
                'name': 'Chitwan',
                'region': 'central',
                'description': 'Home to Chitwan National Park, famous for wildlife and jungle safaris.',
                'altitude': 'lowland',
                'latitude': 27.5598,
                'longitude': 84.4028,
                'best_time_visit': 'October-March',
                'weather_info': 'Warm and humid',
                'distance_from_kathmandu_km': 160,
                'travel_time_hours': 5,
                'primary_attraction': 'Chitwan National Park',
                'emoji': '🐯',
                'popularity_score': 9,
            },
            {
                'name': 'Nagarkot',
                'region': 'east',
                'description': 'A beautiful hilltop destination offering panoramic views of the Himalayas.',
                'altitude': 'mid',
                'latitude': 27.7154,
                'longitude': 85.5244,
                'best_time_visit': 'October-November',
                'weather_info': 'Clear mountain air',
                'distance_from_kathmandu_km': 32,
                'travel_time_hours': 2,
                'primary_attraction': 'Himalayan Views',
                'emoji': '⛰️',
                'popularity_score': 8,
            },
            {
                'name': 'Bhaktapur',
                'region': 'east',
                'description': 'Ancient city near Kathmandu with well-preserved medieval architecture.',
                'altitude': 'mid',
                'latitude': 27.6725,
                'longitude': 85.8294,
                'best_time_visit': 'October-November',
                'weather_info': 'Pleasant and cool',
                'distance_from_kathmandu_km': 15,
                'travel_time_hours': 1,
                'primary_attraction': 'Durbar Square',
                'emoji': '🏰',
                'popularity_score': 8,
            },
        ]

        locations = {}
        for loc_data in locations_data:
            try:
                location = Location.objects.create(**loc_data)
                locations[location.name] = location
                self.stdout.write(
                    self.style.SUCCESS(f'Created location: {location.name}')
                )
            except IntegrityError:
                location = Location.objects.get(name=loc_data['name'])
                locations[location.name] = location

        # Create sample hidden gems
        gems_data = [
            {
                'name': 'Namobuddha',
                'location': 'Bhaktapur',
                'gem_type': 'spiritual',
                'description': 'A deeply spiritual site with Buddhist monasteries and stunning views of the Nepal countryside.',
                'why_special': 'Fewer tourists than major temples, with ancient Buddhist traditions and peaceful atmosphere.',
                'accessibility_level': 3,
                'entry_fee_npr': 200,
                'entry_fee_foreigner_npr': 500,
                'best_time_visit': 'October-November',
                'visit_duration_hours': 4,
                'crowd_level': 'low',
                'rating': 4.7,
            },
            {
                'name': 'Thamel Hidden Courtyard',
                'location': 'Kathmandu',
                'gem_type': 'cultural',
                'description': 'A peaceful courtyard hidden behind busy streets of Thamel with local shops and cafes.',
                'why_special': 'A secret local spot away from tourist crowds, authentic Nepali atmosphere.',
                'accessibility_level': 2,
                'entry_fee_npr': 0,
                'entry_fee_foreigner_npr': 0,
                'best_time_visit': 'Year-round',
                'visit_duration_hours': 2,
                'crowd_level': 'low',
                'rating': 4.5,
            },
            {
                'name': 'Fewa Lake Sunrise Walk',
                'location': 'Pokhara',
                'gem_type': 'natural',
                'description': 'Early morning walk around Fewa Lake with Annapurna views and local fishermen.',
                'why_special': 'Experience authentic morning life with stunning mountain reflections.',
                'accessibility_level': 2,
                'entry_fee_npr': 0,
                'entry_fee_foreigner_npr': 0,
                'best_time_visit': 'October-November',
                'visit_duration_hours': 3,
                'crowd_level': 'medium',
                'rating': 4.6,
            },
            {
                'name': 'Bharatpur Bird Sanctuary',
                'location': 'Chitwan',
                'gem_type': 'natural',
                'description': 'A wetland sanctuary home to migratory and resident birds.',
                'why_special': 'Beautiful birdwatching spot with 400+ bird species.',
                'accessibility_level': 2,
                'entry_fee_npr': 50,
                'entry_fee_foreigner_npr': 100,
                'best_time_visit': 'November-February',
                'visit_duration_hours': 3,
                'crowd_level': 'low',
                'rating': 4.4,
            },
            {
                'name': 'Nagi Ghat Sacred Bathing',
                'location': 'Bhaktapur',
                'gem_type': 'spiritual',
                'description': 'Ancient sacred bathing ghat with local rituals and peaceful riverside setting.',
                'why_special': 'Authentic spiritual experience with local traditions.',
                'accessibility_level': 3,
                'entry_fee_npr': 0,
                'entry_fee_foreigner_npr': 0,
                'best_time_visit': 'Year-round',
                'visit_duration_hours': 2,
                'crowd_level': 'low',
                'rating': 4.3,
            },
            {
                'name': 'Phulchoki Mountain Trek',
                'location': 'Kathmandu',
                'gem_type': 'adventure',
                'description': 'Off-the-beaten-path mountain trek with rhododendron forests.',
                'why_special': 'Peaceful trek with amazing mountain views and fewer tourists.',
                'accessibility_level': 4,
                'entry_fee_npr': 0,
                'entry_fee_foreigner_npr': 0,
                'best_time_visit': 'March-May, September-November',
                'visit_duration_hours': 6,
                'crowd_level': 'low',
                'rating': 4.8,
            },
        ]

        for gem_data in gems_data:
            location_name = gem_data.pop('location')
            location = locations.get(location_name)
            if location:
                try:
                    gem = HiddenGem.objects.create(
                        location=location,
                        **gem_data
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Created hidden gem: {gem.name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating {gem_data["name"]}: {str(e)}')
                    )

        # Create sample local experiences
        self.stdout.write(self.style.SUCCESS('\n--- Creating Local Experiences ---'))
        experiences_data = [
            {
                'name': 'Pottery Workshop in Bhaktapur',
                'location': 'Bhaktapur',
                'category': 'workshop',
                'description': 'Learn traditional Nepali pottery making from a master craftsman. Create your own pottery piece to take home.',
                'duration_hours': 3,
                'cost_per_person_npr': 1200,
                'group_capacity': 5,
                'available_months': '1,2,3,4,5,9,10,11,12',
                'booking_required': True,
                'contact_info': 'Bhaktapur Pottery Guild',
                'what_to_expect': 'You will learn wheel throwing, hand molding, and traditional techniques. All materials provided.',
                'kids_friendly': True,
                'physical_difficulty': 2,
                'rating': 4.8,
            },
            {
                'name': 'Cooking Class & Market Tour',
                'location': 'Kathmandu',
                'category': 'cuisine',
                'description': 'Learn to cook authentic Nepali dishes with a local chef, including a tour of traditional markets.',
                'duration_hours': 4,
                'cost_per_person_npr': 2000,
                'group_capacity': 8,
                'available_months': '1,2,3,4,5,9,10,11,12',
                'booking_required': True,
                'contact_info': 'Kathmandu Culinary Academy',
                'what_to_expect': 'Market tour, hands-on cooking, and enjoy your creations for lunch.',
                'kids_friendly': True,
                'physical_difficulty': 2,
                'rating': 4.9,
            },
            {
                'name': 'Jungle Safari - Chitwan',
                'location': 'Chitwan',
                'category': 'trekking',
                'description': 'Early morning jungle safari to spot tigers, rhinos, and various bird species in their natural habitat.',
                'duration_hours': 5,
                'cost_per_person_npr': 3500,
                'group_capacity': 6,
                'available_months': '10,11,12,1,2,3',
                'booking_required': True,
                'contact_info': 'Chitwan Safari Lodge',
                'what_to_expect': 'Jeep safari, expert guide, wildlife photography opportunities, breakfast included.',
                'kids_friendly': True,
                'physical_difficulty': 2,
                'rating': 4.7,
            },
            {
                'name': 'Lakeside Yoga & Meditation',
                'location': 'Pokhara',
                'category': 'spiritual',
                'description': 'Morning yoga and meditation session on the shores of Phewa Lake with mountain views.',
                'duration_hours': 2,
                'cost_per_person_npr': 1000,
                'group_capacity': 15,
                'available_months': '1,2,3,4,5,9,10,11,12',
                'booking_required': False,
                'contact_info': 'Lotus Yoga Pokhara',
                'what_to_expect': 'Guided yoga, meditation, peaceful lakeside setting, refreshments included.',
                'kids_friendly': True,
                'physical_difficulty': 1,
                'rating': 4.6,
            },
            {
                'name': 'Tea Plantation Tour',
                'location': 'Nagarkot',
                'category': 'market',
                'description': 'Tour a working tea plantation, learn about tea processing, and taste freshly brewed Himalayan tea.',
                'duration_hours': 3,
                'cost_per_person_npr': 1500,
                'group_capacity': 10,
                'available_months': '9,10,11,12,1,2,3,4',
                'booking_required': True,
                'contact_info': 'Himalayan Tea Estate',
                'what_to_expect': 'Plantation walk, tea picking demonstration, tasting from multiple varieties.',
                'kids_friendly': True,
                'physical_difficulty': 2,
                'rating': 4.5,
            },
            {
                'name': 'Homestay Cultural Exchange',
                'location': 'Bhaktapur',
                'category': 'homestay',
                'description': 'Stay with a local family, learn their daily routines, enjoy home-cooked meals, and experience authentic Nepali life.',
                'duration_hours': 24,
                'cost_per_person_npr': 5000,
                'group_capacity': 2,
                'available_months': '1,2,3,4,5,9,10,11,12',
                'booking_required': True,
                'contact_info': 'Bhaktapur Homestay Network',
                'what_to_expect': 'Home-cooked meals, cultural activities, local stories, comfortable room.',
                'kids_friendly': True,
                'physical_difficulty': 1,
                'rating': 4.9,
            },
        ]

        for exp_data in experiences_data:
            location_name = exp_data.pop('location')
            location = locations.get(location_name)
            if location:
                try:
                    experience = LocalExperience.objects.create(
                        location=location,
                        **exp_data
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Created local experience: {experience.name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating experience: {str(e)}')
                    )

        # Create sample seasonal tips
        self.stdout.write(self.style.SUCCESS('\n--- Creating Seasonal Tips ---'))
        seasonal_data = [
            {
                'season': 'spring',
                'month': 3,
                'title': 'Spring Blooms & Clear Skies',
                'description': 'Spring is one of the best times to visit Nepal with rhododendron flowers blooming throughout the hills.',
                'temperature_range_celsius': '15-25°C',
                'rainfall_level': 'low',
                'visibility': 'excellent',
                'risks': 'Strong sunlight at high altitude',
                'recommendations': 'Perfect for trekking. Bring sunscreen. Lightweight layers recommended.',
                'crowd_level': 'high',
                'ideal_activities': 'Trekking, Mountain biking, Photography, Paragliding, Birdwatching',
            },
            {
                'season': 'summer',
                'month': 7,
                'title': 'Monsoon Season Adventures',
                'description': 'The monsoon brings lush green landscapes and fewer tourists. Some trails may be challenging.',
                'temperature_range_celsius': '20-28°C',
                'rainfall_level': 'high',
                'visibility': 'poor',
                'risks': 'Landslides, Flight cancellations, Flooded trails',
                'recommendations': 'Waterproof gear essential. Shorter treks recommended. River activities are popular.',
                'crowd_level': 'low',
                'ideal_activities': 'Wildlife spotting, River rafting, Short treks, Indoor activities',
            },
            {
                'season': 'autumn',
                'month': 10,
                'title': 'Crystal Clear Mountains',
                'description': 'Autumn offers the clearest mountain views and perfect trekking conditions. Very popular season.',
                'temperature_range_celsius': '10-20°C',
                'rainfall_level': 'low',
                'visibility': 'excellent',
                'risks': 'High crowds at popular trails',
                'recommendations': 'Best season overall. Book accommodations early. Bring layers for cool evenings.',
                'crowd_level': 'high',
                'ideal_activities': 'Trekking, Mountain climbing, Photography, Paragliding, Sightseeing',
            },
            {
                'season': 'winter',
                'month': 12,
                'title': 'Crisp & Festival Season',
                'description': 'Winter brings clear skies and cool weather. Perfect for cultural festivals and lowland exploration.',
                'temperature_range_celsius': '5-15°C',
                'rainfall_level': 'low',
                'visibility': 'good',
                'risks': 'Cold temperatures in highlands, Occasional snow',
                'recommendations': 'Warm clothing essential. Excellent for cultural activities. Lower elevation treks best.',
                'crowd_level': 'medium',
                'ideal_activities': 'Festivals, Temple visiting, Lowland treks, Cultural tours, Hot springs',
            },
        ]

        for season_data in seasonal_data:
            try:
                season_tip = SeasonalTip.objects.create(**season_data)
                self.stdout.write(
                    self.style.SUCCESS(f'Created seasonal tip: {season_tip.title}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating seasonal tip: {str(e)}')
                )

        # Create sample budget tips
        self.stdout.write(self.style.SUCCESS('\n--- Creating Budget Tips ---'))
        budget_data = [
            {
                'title': 'Eat at Local Dhaba Restaurants',
                'category': 'food',
                'budget_level': 'budget',
                'content': 'Skip tourist restaurants and eat where locals eat. A full meal at a dhaba costs only NPR 100-300.',
                'tip_shorthand': 'Eat at dhabas for authentic, cheap meals',
                'effectiveness_score': 9,
                'relevant_location': None,
            },
            {
                'title': 'Use Local Transportation',
                'category': 'transport',
                'budget_level': 'budget',
                'content': 'Instead of taxis, use buses, minibuses (micros), or shared jeeps. Much cheaper and authentic experience.',
                'tip_shorthand': 'Use buses instead of taxis',
                'effectiveness_score': 9,
                'relevant_location': None,
            },
            {
                'title': 'Stay in Hostels or Guesthouses',
                'category': 'accommodation',
                'budget_level': 'budget',
                'content': 'Clean hostels offer dorm beds for NPR 400-800. Mix with other travelers and get local recommendations.',
                'tip_shorthand': 'Choose hostels over hotels',
                'effectiveness_score': 9,
                'relevant_location': None,
            },
            {
                'title': 'Visit Free or Low-Cost Temples',
                'category': 'activities',
                'budget_level': 'budget',
                'content': 'Many temples have free entry. Donation-based entries typically NPR 50-100. Beautiful and meaningful experiences.',
                'tip_shorthand': 'Free temple visits available',
                'effectiveness_score': 8,
                'relevant_location': None,
            },
            {
                'title': 'Buy from Local Markets',
                'category': 'shopping',
                'budget_level': 'budget',
                'content': 'Shop at Asan Bazaar and Indra Bazaar instead of tourist shops. Get better prices and support locals.',
                'tip_shorthand': 'Shop at local bazaars for deals',
                'effectiveness_score': 9,
                'relevant_location': None,
            },
            {
                'title': 'Mid-Range Hotel Tips',
                'category': 'accommodation',
                'budget_level': 'mid',
                'content': 'Look for 3-star hotels with good reviews. Prices NPR 2500-5000 per night. Negotiate for longer stays.',
                'tip_shorthand': '3-star hotels offer best value',
                'effectiveness_score': 8,
                'relevant_location': None,
            },
            {
                'title': 'Restaurant Selection Strategy',
                'category': 'food',
                'budget_level': 'mid',
                'content': 'Mix local restaurants with mid-range tourist restaurants. Saves money while enjoying good variety.',
                'tip_shorthand': 'Mix local and mid-range restaurants',
                'effectiveness_score': 8,
                'relevant_location': None,
            },
            {
                'title': 'Luxury Hotel Booking Tips',
                'category': 'accommodation',
                'budget_level': 'luxury',
                'content': 'Book luxury hotels directly or through hotel websites. Apps often cheaper than booking sites.',
                'tip_shorthand': 'Direct booking often cheaper',
                'effectiveness_score': 7,
                'relevant_location': None,
            },
            {
                'title': 'Plan Activities in Groups',
                'category': 'activities',
                'budget_level': 'all',
                'content': 'Group activities and tours cost less per person. Join group treks and shared tours.',
                'tip_shorthand': 'Group activities are cheaper',
                'effectiveness_score': 8,
                'relevant_location': None,
            },
            {
                'title': 'Best Time for Budget Deals',
                'category': 'general',
                'budget_level': 'all',
                'content': 'Visit during monsoon season (July-August) for cheaper rates. Hotels offer 30-50% discounts.',
                'tip_shorthand': 'Travel in monsoon for discounts',
                'effectiveness_score': 9,
                'relevant_location': None,
            },
        ]

        for budget_tip_data in budget_data:
            try:
                budget_tip = BudgetTip.objects.create(**budget_tip_data)
                self.stdout.write(
                    self.style.SUCCESS(f'Created budget tip: {budget_tip.title}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating budget tip: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS('\n✅ Database populated successfully with comprehensive data!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✅ Total Locations: {Location.objects.count()}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✅ Total Hidden Gems: {HiddenGem.objects.count()}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✅ Total Local Experiences: {LocalExperience.objects.count()}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✅ Total Seasonal Tips: {SeasonalTip.objects.count()}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✅ Total Budget Tips: {BudgetTip.objects.count()}')
        )
