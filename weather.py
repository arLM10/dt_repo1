from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock weather data for cities
weather_data = {
    "London": {
        "current": {
            "temperature": "15°C",
            "condition": "Cloudy",
            "humidity": "70%"
        },
        "forecast": [
            {"day": "Monday", "temperature": "14°C", "condition": "Rainy"},
            {"day": "Tuesday", "temperature": "16°C", "condition": "Partly Cloudy"},
            {"day": "Wednesday", "temperature": "17°C", "condition": "Sunny"}
        ]
    },
    "Paris": {
        "current": {
            "temperature": "20°C",
            "condition": "Clear",
            "humidity": "60%"
        },
        "forecast": [
            {"day": "Monday", "temperature": "19°C", "condition": "Sunny"},
            {"day": "Tuesday", "temperature": "21°C", "condition": "Clear"},
            {"day": "Wednesday", "temperature": "22°C", "condition": "Sunny"}
        ]
    }
}


# ---------------------------
# WEATHER API MOCK ENDPOINTS
# ---------------------------

# Get current weather for a city
@app.route('/api/weather/current', methods=['GET'])
def get_current_weather():
    city = request.args.get('city')

    if city in weather_data:
        return jsonify(weather_data[city]["current"]), 200
    else:
        return jsonify({"error": "City not found"}), 404


# Get 3-day forecast for a city
@app.route('/api/weather/forecast', methods=['GET'])
def get_weather_forecast():
    city = request.args.get('city')
    days = request.args.get('days', default=3, type=int)

    if city in weather_data:
        forecast = weather_data[city]["forecast"][:days]
        return jsonify(forecast), 200
    else:
        return jsonify({"error": "City not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)