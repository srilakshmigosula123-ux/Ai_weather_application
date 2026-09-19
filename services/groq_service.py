"""Groq-powered weather summary generation."""

from typing import Any


# Groq's current replacement for the retired llama-3.1-8b-instant model.
MODEL = "openai/gpt-oss-20b"


def explain_weather(weather: dict[str, Any], api_key: str) -> str:
    """Return a concise friendly summary, with a local fallback on AI failures."""
    fallback = (
        f"Expect {weather['condition'].lower()} conditions in {weather['city']}. "
        f"It is {weather['temperature']} degrees C with {weather['humidity']}% humidity "
        f"and wind around {weather['wind_speed']} km/h."
    )
    if not api_key or api_key == "your_groq_api_key":
        return fallback

    try:
        from groq import Groq

        completion = Groq(api_key=api_key).chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Give a warm, practical weather summary in one or two sentences. "
                        "Use only the supplied weather data."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"City: {weather['city']}\nCondition: {weather['condition']}\n"
                        f"Temperature: {weather['temperature']} C\n"
                        f"Feels like: {weather['feels_like']} C\n"
                        f"Humidity: {weather['humidity']}%\n"
                        f"Wind: {weather['wind_speed']} km/h"
                    ),
                },
            ],
            temperature=0.4,
            max_completion_tokens=100,
        )
        content = completion.choices[0].message.content
        return content.strip() if content else fallback
    except Exception:
        return fallback
