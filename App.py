from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import random  # Import the random module

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- New Mood to Destination Mapping ---
# Each mood now maps to a list of possible destinations.
MOOD_MAP = {
    'adventure': [
        'Queenstown, New Zealand',
        'Zermatt, Switzerland',
        'Patagonia, Argentina'
    ],
    'relaxing': [
        'Bora Bora, French Polynesia',
        'Maldives',
        'Kyoto, Japan'
    ],
    'romantic': [
        'Paris, France',
        'Venice, Italy',
        'Santorini, Greece'
    ],
    'cultural': [
        'Kyoto, Japan',
        'Rome, Italy',
        'Istanbul, Turkey'
    ],
    'party': [
        'Ibiza, Spain',
        'Las Vegas, USA',
        'Mykonos, Greece'
    ]
}

# API Keys from your .env file
OPENWEATHER_API_KEY = os.getenv('11d5a20b68034e2695d121200251609')

# --- New API Endpoint ---
@app.route('/plan', methods=['GET'])
def plan_trip():
    """
    New endpoint to plan a trip and render an HTML page.
    """
    user_mood = request.args.get('mood', '').lower()

    if user_mood not in MOOD_MAP:
        return "Invalid mood provided.", 400

    # Randomly select a destination from the list for the given mood
    destination = random.choice(MOOD_MAP[user_mood])

    try:
        weather = get_weather_data(destination)
        attractions = get_static_places_data(destination, 'attraction')
        hotels = get_static_places_data(destination, 'hotel')
        itinerary = generate_itinerary(destination)

        return render_template(
            'results.html',
            destination=destination,
            attractions=attractions,
            hotels=hotels,
            weather=weather,
            itinerary=itinerary
        )
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

# --- Helper Functions (Updated to include new destinations) ---
def get_static_places_data(location, place_type):
    """
    Returns hard-coded data as an alternative to a paid API.
    """
    data = {
        'Queenstown, New Zealand': {
            'attraction': [{'name': 'Skyline Queenstown'}, {'name': 'Shotover Jet'}],
            'hotel': [{'name': 'QT Queenstown'}, {'name': 'Novotel Queenstown'}]
        },
        'Zermatt, Switzerland': {
            'attraction': [{'name': 'Matterhorn Mountain'}, {'name': 'Gornergrat Bahn'}],
            'hotel': [{'name': 'Mont Cervin Palace'}, {'name': 'Hotel Cervo'}]
        },
        'Patagonia, Argentina': {
            'attraction': [{'name': 'Perito Moreno Glacier'}, {'name': 'Fitz Roy Trail'}],
            'hotel': [{'name': 'Arakur Ushuaia'}, {'name': 'The Singular Patagonia'}]
        },
        'Bora Bora, French Polynesia': {
            'attraction': [{'name': 'Mount Otemanu'}, {'name': 'Matira Beach'}],
            'hotel': [{'name': 'St. Regis Bora Bora'}, {'name': 'InterContinental Bora Bora'}]
        },
        'Maldives': {
            'attraction': [{'name': 'Male Atoll'}, {'name': 'Banana Reef'}],
            'hotel': [{'name': 'Soneva Fushi'}, {'name': 'W Maldives'}]
        },
        'Paris, France': {
            'attraction': [{'name': 'Eiffel Tower'}, {'name': 'Louvre Museum'}],
            'hotel': [{'name': 'Hôtel Plaza Athénée'}, {'name': 'Le Meurice'}]
        },
        'Venice, Italy': {
            'attraction': [{'name': 'Grand Canal'}, {'name': 'St. Mark\'s Basilica'}],
            'hotel': [{'name': 'Gritti Palace'}, {'name': 'The St. Regis Venice'}]
        },
        'Santorini, Greece': {
            'attraction': [{'name': 'Oia Village'}, {'name': 'Ancient Thera'}],
            'hotel': [{'name': 'Grace Hotel Santorini'}, {'name': 'Canaves Oia Suites'}]
        },
        'Kyoto, Japan': {
            'attraction': [{'name': 'Kinkaku-ji'}, {'name': 'Fushimi Inari-taisha'}],
            'hotel': [{'name': 'Ritz-Carlton Kyoto'}, {'name': 'Hyatt Regency Kyoto'}]
        },
        'Rome, Italy': {
            'attraction': [{'name': 'Colosseum'}, {'name': 'Vatican City'}],
            'hotel': [{'name': 'The St. Regis Rome'}, {'name': 'J.K. Place Roma'}]
        },
        'Istanbul, Turkey': {
            'attraction': [{'name': 'Hagia Sophia'}, {'name': 'Grand Bazaar'}],
            'hotel': [{'name': 'Ciragan Palace Kempinski'}, {'name': 'Four Seasons Istanbul'}]
        },
        'Ibiza, Spain': {
            'attraction': [{'name': 'Es Vedra'}, {'name': 'Dalt Vila'}],
            'hotel': [{'name': 'Ushuaïa Ibiza Beach Hotel'}, {'name': 'Hard Rock Hotel Ibiza'}]
        },
        'Las Vegas, USA': {
            'attraction': [{'name': 'Las Vegas Strip'}, {'name': 'Fountains of Bellagio'}],
            'hotel': [{'name': 'Caesars Palace'}, {'name': 'The Cosmopolitan'}]
        },
        'Mykonos, Greece': {
            'attraction': [{'name': 'Little Venice'}, {'name': 'Windmills of Mykonos'}],
            'hotel': [{'name': 'Myconian Ambassador'}, {'name': 'Cavo Tagoo Mykonos'}]
        }
    }
    return data.get(location, {}).get(place_type, [])

# New helper function for the WeatherAPI service
def get_weather_data(location):
    """
    Fetches weather data from the WeatherAPI.com service.
    """
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': '11d5a20b68034e2695d121200251609',
        'q': location
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        temp = data['current']['temp_c']
        condition = data['current']['condition']['text']
        return {'temperature': f"{temp}°C", 'condition': condition}
    except Exception as e:
        print(f"Error fetching weather data from WeatherAPI: {e}")
        return {'temperature': 'N/A', 'condition': 'Weather not available'}

def generate_itinerary(destination):
    """
    Generates a simple, predefined itinerary based on the destination.
    """
    itineraries = {
        'Paris, France': [
            'Day 1: Arrive and see the Eiffel Tower',
            'Day 2: Visit the Louvre Museum',
            'Day 3: Take a stroll along the River Seine'
        ],
        'Venice, Italy': [
            'Day 1: Explore St. Mark\'s Square and Basilica',
            'Day 2: Take a gondola ride through the canals',
            'Day 3: Visit the Rialto Bridge and market'
        ],
        'Santorini, Greece': [
            'Day 1: Explore the famous blue domes of Oia',
            'Day 2: Relax on the unique Red Beach',
            'Day 3: Watch the sunset over the caldera'
        ],
        'Bora Bora, French Polynesia': [
            'Day 1: Arrive and relax on Matira Beach',
            'Day 2: Go snorkeling in the coral gardens',
            'Day 3: Explore Mount Otemanu'
        ],
        'Maldives': [
            'Day 1: Settle into your overwater bungalow',
            'Day 2: Snorkel or dive among coral reefs',
            'Day 3: Enjoy a sunset cruise'
        ],
        'Kyoto, Japan': [
            'Day 1: Visit the Fushimi Inari-taisha shrine',
            'Day 2: Explore the Gion district',
            'Day 3: Find a quiet Zen garden'
        ],
        'Rome, Italy': [
            'Day 1: Arrive and see the Colosseum and Roman Forum',
            'Day 2: Explore Vatican City and St. Peter\'s Basilica',
            'Day 3: Make a wish at the Trevi Fountain'
        ],
        'Istanbul, Turkey': [
            'Day 1: Visit the Hagia Sophia and Blue Mosque',
            'Day 2: Explore the Grand Bazaar and Spice Market',
            'Day 3: Take a Bosphorus cruise'
        ],
        'Queenstown, New Zealand': [
            'Day 1: Go for a scenic gondola ride',
            'Day 2: Try bungee jumping or a jet boat ride',
            'Day 3: Hike one of the scenic trails'
        ],
        'Zermatt, Switzerland': [
            'Day 1: Take the cable car to see the Matterhorn',
            'Day 2: Go skiing or snowboarding',
            'Day 3: Explore the village and visit the museum'
        ],
        'Patagonia, Argentina': [
            'Day 1: Trek to see the Perito Moreno Glacier',
            'Day 2: Hike the Fitz Roy Trail in El Chaltén',
            'Day 3: Explore the town of Ushuaia'
        ],
        'Ibiza, Spain': [
            'Day 1: Explore the historic Dalt Vila',
            'Day 2: Spend the day at a beach club',
            'Day 3: Experience the vibrant nightlife'
        ],
        'Las Vegas, USA': [
            'Day 1: Walk the famous Strip and see the Fountains of Bellagio',
            'Day 2: See a world-class show or concert',
            'Day 3: Take a day trip to the Grand Canyon'
        ],
        'Mykonos, Greece': [
            'Day 1: Explore the iconic windmills and Little Venice',
            'Day 2: Spend the day at Paradise or Super Paradise Beach',
            'Day 3: Enjoy the island\'s vibrant nightlife'
        ]
    }
    return itineraries.get(destination, [])
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)