import webbrowser
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
# Define your OpenWeatherMap API Key here temporarily
OPENWEATHER_API_KEY = "ebc85e3b4f63ce523a96786c1bfd55fc"
import requests
import json # Good practice to import if you're dealing with JSON

def get_current_weather(city_name, api_key, units="metric"):
    """
    Fetches current weather data for a specific city using OpenWeatherMap Current Weather Data API (v2.5).

    Args:
        city_name (str): The name of the city.
        api_key (str): Your OpenWeatherMap API key.
        units (str, optional): Units for temperature. 'metric' for Celsius,
                               'imperial' for Fahrenheit, 'standard' for Kelvin.
                               Defaults to 'metric'.

    Returns:
        dict: Current weather data as a Python dictionary if successful, None otherwise.
    """
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': city_name,
        'appid': api_key,
        'units': units
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

        weather_data = response.json()
        return weather_data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}") # Print full response for debugging
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred: {req_err}")
        return None
    except json.JSONDecodeError: # Catch if response.json() fails (e.g., non-JSON response)
        print(f"Error decoding JSON from response: {response.text}")
        return None



@app.route('/')
def hello():
    return "Hellooooo"

@app.route('/api/current-weather', methods=['GET'])
def get_weather():
    # Step 1: Get the city name from the URL query parameters
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "City parameter is missing"}), 400

    # Step 2: Use your get_current_weather function
    weather_data = get_current_weather(city, OPENWEATHER_API_KEY) 

    # Step 3: Return the data as JSON
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Could not retrieve weather data"}), 500



if __name__=='__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)
