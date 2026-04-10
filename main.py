from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
import os

app = FastAPI(title="Weather App")

# Serve the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Paste your OpenWeatherMap API key here ---
API_KEY = "6867c0ebed3d3b47b931ea11428736ba"
BASE_URL = "https://api.openweathermap.org/data/2.5"


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/weather")
async def get_weather(city: str):
    """Get current weather for a city."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/weather",
            params={
                "q": city,
                "appid": API_KEY,
                "units": "imperial"  # Change to "metric" for Celsius
            }
        )

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Weather API error")

    data = response.json()

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "temp_min": round(data["main"]["temp_min"]),
        "temp_max": round(data["main"]["temp_max"]),
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].title(),
        "icon": data["weather"][0]["icon"],
        "wind_speed": round(data["wind"]["speed"]),
        "visibility": round(data.get("visibility", 0) / 1609, 1),  # meters to miles
    }


@app.get("/forecast")
async def get_forecast(city: str):
    """Get 5-day forecast for a city (every 3 hours, we grab one per day)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/forecast",
            params={
                "q": city,
                "appid": API_KEY,
                "units": "imperial"
            }
        )

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Weather API error")

    data = response.json()

    # Grab one forecast entry per unique day (at noon-ish)
    seen_dates = set()
    forecast = []
    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        time = entry["dt_txt"].split(" ")[1]
        if date not in seen_dates and time >= "12:00:00":
            seen_dates.add(date)
            forecast.append({
                "date": date,
                "temp_max": round(entry["main"]["temp_max"]),
                "temp_min": round(entry["main"]["temp_min"]),
                "description": entry["weather"][0]["description"].title(),
                "icon": entry["weather"][0]["icon"],
            })
        if len(forecast) == 5:
            break

    return {"city": data["city"]["name"], "forecast": forecast}
