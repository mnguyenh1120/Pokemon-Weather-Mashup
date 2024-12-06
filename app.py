import functions
from flask import Flask, render_template, request
import urllib.parse, urllib.request, urllib.error, json
import pprint
from keys import api_key1

# Create an instance of Flask
app = Flask(__name__)

@app.route('/')
def home():
    try:
        data = functions.get_city_data()
        print("DEBUG: Data returned by get_city_data:", data)
        return render_template("index.html", data=data)
    except Exception as e:
        print(f"Error in home route: {e}")
        return "An error occurred while processing your request.", 500

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()  # Get the search query and strip whitespace
    if not query:
        return render_template('results.html', error="Please enter a city name.")

    try:
        # Fetch the geolocation for the city
        coordinates = functions.geolocation_finder(query, api_key1)
        if not coordinates:
            return render_template(
                'results.html',
                error=f"Sorry, no results were found for your query: '{query}'",
                place=query
            )

        # Fetch weather data
        current_forecast_data = functions.get_current_forecast(coordinates, api_key1)
        if not current_forecast_data:
            return render_template(
                'results.html',
                error="Unable to fetch weather data. Please try again.",
                place=query
            )

        # Extract weather condition and temperature
        weather_condition = current_forecast_data['weather'][0]['main']
        temperature = round(current_forecast_data['main']['temp'])
        iconid = current_forecast_data['weather'][0]['icon']
        icon_url = functions.weather_icon(iconid)

        # Fetch Pokémon based on weather
        pokemon_list = functions.get_types_for_weather(weather_condition)
        pokemon_pair_data = functions.randomized_pokemon(pokemon_list)

        # Prepare data for the results template
        result_data = {
            "city": query,
            "pokemon": pokemon_pair_data,
            "temperature": temperature,
            "condition": weather_condition,
            "icon": icon_url,
        }

        return render_template('results.html', data=[result_data])  # Wrap result in a list for consistency

    except Exception as e:
        print(f"Error in search route: {e}")
        return render_template('results.html', error="An error occurred while processing your request.")


if __name__ == "__main__":
    app.run(debug=True)
