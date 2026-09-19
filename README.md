# AI Weather App

A Flask web app that fetches real-time weather from OpenWeatherMap and turns it into a friendly summary using Groq.

## Setup

1. Create an [OpenWeatherMap API key](https://openweathermap.org/api) and a [Groq API key](https://console.groq.com/keys).
2. Add the keys to `.env`. Keep this file private; it is intentionally ignored by Git.
3. In a terminal, run:

```powershell
cd ai-weather-app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

If the Groq key is omitted or unavailable, the app still displays a useful built-in weather summary. The weather API key is required for live data.
