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

# --- Main execution part ---
if __name__ == "__main__":
    # TODO: Replace with your actual API key from OpenWeatherMap
    YOUR_API_KEY = "ebc85e3b4f63ce523a96786c1bfd55fc"

    # --- Test with a city ---
    city_to_check = "Pune" # Let's stick with Pune for now

    print(f"Fetching current weather for {city_to_check}...")
    current_weather = get_current_weather(city_to_check, YOUR_API_KEY, units="metric")

    if current_weather:
        print("\n--- Raw Weather Data ---")
        # Use json.dumps for pretty printing the JSON
        print(json.dumps(current_weather, indent=4))

        # Example of extracting specific data points
        print(f"\n--- Processed Weather Data for {city_to_check} ---")
        main_data = current_weather.get('main', {})
        weather_description = current_weather.get('weather', [{}])[0].get('description', 'N/A')
        temperature = main_data.get('temp', 'N/A')
        feels_like = main_data.get('feels_like', 'N/A')
        humidity = main_data.get('humidity', 'N/A')
        wind_speed = current_weather.get('wind', {}).get('speed', 'N/A')
        country = current_weather.get('sys', {}).get('country', 'N/A')

        print(f"Location: {current_weather.get('name', 'N/A')}, {country}")
        print(f"Temperature: {temperature}°C (feels like {feels_like}°C)")
        print(f"Description: {weather_description.capitalize()}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
    else:
        print(f"Failed to retrieve weather data for {city_to_check}.")

    # You can try another city here if you like
    # print("\nFetching current weather for London...")
    # london_weather = get_current_weather("London", YOUR_API_KEY, units="imperial")
    # if london_weather:
    #     print(json.dumps(london_weather, indent=4))
    # else:
    #     print("Failed to retrieve weather data for London.")