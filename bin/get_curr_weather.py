import requests
import json
def get_weather_data():
    url = "https://api.weather.gov/stations/KDWH/observations/latest"
    headers = {'User-Agent': 'bird.camera', 'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200:
        temp_fahrenheit = round(data['properties']['temperature']['value'] * 9/5 + 32,1)
        relative_humidity = round(data['properties']['relativeHumidity']['value'],1)
        heat_index = round(data['properties']['heatIndex']['value'] * 9/5 + 32,1) if data['properties']['heatIndex']['value'] is not None else None
        wind_speed = data['properties']['windSpeed']['value']
        wind_direction_degrees = data['properties']['windDirection']['value']
        if wind_speed == 0 or wind_direction_degrees is None:
            wind_direction = None
        else:
            wind_direction_degrees = data['properties']['windDirection']['value']
            cardinal_directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
            index = round(wind_direction_degrees / 45)
            wind_direction = cardinal_directions[index]


        return {
            "temperature": temp_fahrenheit,
            "relativeHumidity": relative_humidity,
            "heatIndex": heat_index,
            "windSpeed": wind_speed,
            "windDirection": wind_direction
        }
    else:
        print("Error fetching weather data:", response.status_code)
        return None

def main():
    weather_data = get_weather_data()
    if weather_data:
        formatted_data = json.dumps(weather_data, indent=2)
        with open("/var/www/html/current_weather.json", "w") as f:
            f.write(formatted_data)
    else:
        print("Error fetching weather data")

if __name__ == '__main__':
    main()