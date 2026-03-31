#!/usr/bin/env python3
"""
Weather data fetcher for bird.camera project.

Fetches current weather data from weather.gov API and saves it as JSON
for use by the web application.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, Optional, Union

import requests

# Configuration constants
API_URL = "https://api.weather.gov/stations/KDWH/observations/latest"
OUTPUT_FILE = "/var/www/html/current_weather.json"
REQUEST_TIMEOUT = 10  # seconds
USER_AGENT = "bird.camera"

# Wind direction mapping
CARDINAL_DIRECTIONS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def celsius_to_fahrenheit(celsius: Optional[float]) -> Optional[float]:
    """Convert Celsius to Fahrenheit."""
    if celsius is None:
        return None
    return round(celsius * 9/5 + 32, 1)


def degrees_to_cardinal(degrees: Optional[float]) -> Optional[str]:
    """Convert wind direction degrees to cardinal direction."""
    if degrees is None:
        return None
    
    # Normalize degrees to 0-360 range
    degrees = degrees % 360
    index = round(degrees / 45) % 8
    return CARDINAL_DIRECTIONS[index]


def extract_weather_data(api_response: Dict) -> Dict[str, Union[float, str, None]]:
    """Extract and process weather data from API response."""
    try:
        properties = api_response.get('properties', {})
        
        # Extract raw values with safe access
        temp_celsius = properties.get('temperature', {}).get('value')
        humidity = properties.get('relativeHumidity', {}).get('value')
        heat_index_celsius = properties.get('heatIndex', {}).get('value')
        wind_speed = properties.get('windSpeed', {}).get('value')
        wind_direction_degrees = properties.get('windDirection', {}).get('value')
        
        # Process the data
        temp_fahrenheit = celsius_to_fahrenheit(temp_celsius)
        relative_humidity = round(humidity, 1) if humidity is not None else None
        heat_index = celsius_to_fahrenheit(heat_index_celsius)
        
        # Handle wind direction (only if wind speed > 0)
        wind_direction = None
        if wind_speed and wind_speed > 0:
            wind_direction = degrees_to_cardinal(wind_direction_degrees)
        
        return {
            "temperature": temp_fahrenheit,
            "relativeHumidity": relative_humidity,
            "heatIndex": heat_index,
            "windSpeed": wind_speed,
            "windDirection": wind_direction
        }
        
    except (KeyError, TypeError, AttributeError) as e:
        logger.error(f"Error processing weather data: {e}")
        raise ValueError(f"Invalid API response structure: {e}")


def fetch_weather_data() -> Optional[Dict]:
    """Fetch weather data from the API."""
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'application/json'
    }
    
    try:
        logger.info(f"Fetching weather data from {API_URL}")
        response = requests.get(API_URL, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        data = response.json()
        return extract_weather_data(data)
        
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("Connection error - check network connectivity")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Error parsing response: {e}")
        return None


def save_weather_data(weather_data: Dict, output_path: str = OUTPUT_FILE) -> bool:
    """Save weather data to JSON file."""
    try:
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        formatted_data = json.dumps(weather_data, indent=2)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_data)
        
        logger.info(f"Weather data saved to {output_path}")
        return True
        
    except (IOError, OSError) as e:
        logger.error(f"Failed to save weather data: {e}")
        return False


def main() -> int:
    """Main function."""
    try:
        weather_data = fetch_weather_data()
        
        if weather_data is None:
            logger.error("Failed to fetch weather data")
            return 1
        
        if not save_weather_data(weather_data):
            logger.error("Failed to save weather data")
            return 1
        
        logger.info("Weather data updated successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())