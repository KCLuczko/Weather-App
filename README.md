# Weather App

A FastAPI backend + HTML frontend weather app using the OpenWeatherMap API.
No database required.

## Setup

### 1. Get a free API key
Go to https://openweathermap.org/api → sign up → copy your API key.
(It takes about 10 minutes to activate after signup)

### 2. Install dependencies
```bash
pip install fastapi uvicorn httpx
```

### 3. Add your API key
Open `main.py` and replace `YOUR_API_KEY` with your actual key:
```python
API_KEY = "abc123yourkeyhere"
```

### 4. Run it
```bash
uvicorn main:app --reload
```

### 5. Open it
Go to http://127.0.0.1:8000 in your browser.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/weather?city=Chicago` | Current weather for a city |
| GET | `/forecast?city=Chicago` | 5-day forecast |
| GET | `/docs` | Swagger UI |

## Project Structure
```
weather-app/
├── main.py          # FastAPI app and endpoints
├── static/
│   └── index.html   # Frontend UI
└── README.md
```

## Switching to Celsius
In `main.py`, change `"units": "imperial"` to `"units": "metric"` in both endpoints.
Then update the `°F` labels in `index.html` to `°C`.
