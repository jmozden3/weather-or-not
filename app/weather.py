import requests
from datetime import datetime

# Get coordinates using OpenStreetMap's Nominatim
def get_coordinates(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    response = requests.get(url, params=params, headers={"User-Agent": "WeatherOrNotApp"})
    data = response.json()

    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    else:
        return None, None

# Get historical weather from Open-Meteo
def get_weather_data(lat, lon, date_str):
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date_str,
        "end_date": date_str,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,sunrise,sunset",
        "timezone": "auto",
        "temperature_unit": "fahrenheit"
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if "daily" not in data:
        return None

    daily = data["daily"]

    return {
        "high": int(daily["temperature_2m_max"][0]),
        "low": int(daily["temperature_2m_min"][0]),
        "rain": "yes" if daily["precipitation_sum"][0] > 0 else "no",
        "sunrise": format_time(daily["sunrise"][0]),
        "sunset": format_time(daily["sunset"][0])
    }

# Convert time from ISO string to readable format
def format_time(iso_string):
    time_obj = datetime.fromisoformat(iso_string)
    return time_obj.strftime("%I:%M%p").lstrip("0").lower()

# Convert '6:45am' to total minutes
def time_to_minutes(time_str):
    dt = datetime.strptime(time_str.strip().lower(), "%I:%M%p")
    return dt.hour * 60 + dt.minute

# Score the user
def calculate_score(user, actual):
    score = 0

    # High Temp — max 25
    high_diff = abs(user["high"] - actual["high"])
    score += max(0, 25 - high_diff)

    # Low Temp — max 25
    low_diff = abs(user["low"] - actual["low"])
    score += max(0, 25 - low_diff)

    # Rain — exact match = 10 points
    if user["rain"] == actual["rain"]:
        score += 10

    # Sunrise & Sunset — max 20 each
    try:
        sunrise_diff = abs(time_to_minutes(user["sunrise"]) - time_to_minutes(actual["sunrise"]))
        score += max(0, 20 - (sunrise_diff // 6))

        sunset_diff = abs(time_to_minutes(user["sunset"]) - time_to_minutes(actual["sunset"]))
        score += max(0, 20 - (sunset_diff // 6))
    except:
        pass

    return int(score)
