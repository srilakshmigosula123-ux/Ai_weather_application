"""Flask entry point for the AI Weather App."""

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from services.groq_service import explain_weather
from services.weather_service import WeatherServiceError, get_weather


PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/weather")
def weather():
    payload = request.get_json(silent=True) or {}
    city = str(payload.get("city", "")).strip()

    if not city:
        return jsonify({"error": "Please enter a city name."}), 400
    if len(city) > 100:
        return jsonify({"error": "City name must be 100 characters or fewer."}), 400

    try:
        weather_data = get_weather(city, os.getenv("OPENWEATHER_API_KEY", ""))
        weather_data["explanation"] = explain_weather(
            weather_data, os.getenv("GROQ_API_KEY", "")
        )
        return jsonify(weather_data)
    except WeatherServiceError as error:
        return jsonify({"error": str(error)}), error.status_code
    except Exception:
        app.logger.exception("Unexpected error while fetching weather")
        return jsonify({"error": "Something went wrong. Please try again."}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=os.getenv("FLASK_DEBUG") == "1")
