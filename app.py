import webbrowser
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json # Good practice to import if you're dealing with JSON

app = Flask(__name__)
CORS(app)

# Define your OpenWeatherMap API Key here temporarily
OPENWEATHER_API_KEY = "ebc85e3b4f63ce523a96786c1bfd55fc"


def get_current_weather(city_name, api_key, units="metric"):
    """
    Fetches current weather data for a specific city.
    """
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': city_name,
        'appid': api_key,
        'units': units
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data

    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred: {req_err}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from response: {response.text}")
        return None


def get_five_day_forecast(city_name, api_key, units="metric"):
    """
    Fetches 5-day forecast data for a specific city.
    """
    BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        'q': city_name,
        'appid': api_key,
        'units': units
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred: {req_err}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from response: {response.text}")
        return None


@app.route('/')
def hello():
    return "Hellooooo"

@app.route('/api/current-weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is missing"}), 400

    weather_data = get_current_weather(city, OPENWEATHER_API_KEY)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Could not retrieve weather data"}), 500

# NEW: The 5-day forecast endpoint
@app.route('/api/five-day-forecast', methods=['GET'])
def get_forecast():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is missing"}), 400

    forecast_data = get_five_day_forecast(city, OPENWEATHER_API_KEY)
    if forecast_data:
        return jsonify(forecast_data)
    else:
        return jsonify({"error": "Could not retrieve forecast data"}), 500


if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)