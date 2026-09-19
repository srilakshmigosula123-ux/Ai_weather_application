"""OpenWeatherMap integration."""

from typing import Any

import requests


WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherServiceError(Exception):
    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.status_code = status_code


def get_weather(city: str, api_key: str) -> dict[str, Any]:
    if not api_key or api_key == "your_openweathermap_api_key":
        raise WeatherServiceError(
            "OpenWeatherMap API key is missing. Add it to .env.", 500
        )

    try:
        response = requests.get(
            WEATHER_URL,
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=10,
        )
    except requests.RequestException as error:
        raise WeatherServiceError("Weather service is currently unavailable.") from error

    if response.status_code == 404:
        raise WeatherServiceError("City not found. Check the spelling and try again.", 404)
    if response.status_code in (401, 403):
        raise WeatherServiceError("The OpenWeatherMap API key is invalid.", 500)
    if response.status_code == 429:
        raise WeatherServiceError("Too many weather requests. Please try again shortly.", 429)
    if not response.ok:
        raise WeatherServiceError("Unable to fetch weather data right now.")

    try:
        data = response.json()
        details = data["weather"][0]
        main = data["main"]
        wind = data["wind"]
        system = data["sys"]
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise WeatherServiceError("Weather service returned incomplete data.") from error

    return {
        "city": data["name"],
        "country": system.get("country", ""),
        "temperature": round(main["temp"]),
        "feels_like": round(main["feels_like"]),
        "humidity": main["humidity"],
        "wind_speed": round(wind["speed"] * 3.6, 1),
        "condition": details["description"].title(),
        "icon": details["icon"],
    }
