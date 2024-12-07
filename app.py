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
    query = request.args.get('query', '').strip()  # Get the search query
    # data = functions.get_city_data(query)
    # return render_template("result.html", data=data)
    print(f"DEBUG: Received search query: {query}")  # Log the query
    if not query:
        return render_template('results.html', error="Please enter a city name.")

    try:
        # Fetch the weather data for the city
        coordinates = functions.geolocation_finder(query, api_key1)
        print(f"DEBUG: Coordinates fetched: {coordinates}")  # Log coordinates
        if not coordinates:
            return render_template('results.html', error=f"No data found for city: {query}")

        current_forecast_data = functions.get_current_forecast(coordinates, api_key1)
        print(f"DEBUG: Current forecast data: {current_forecast_data}")  # Log forecast data
        if not current_forecast_data:
            return render_template('results.html', error="Unable to fetch weather data.")

        # Extract weather condition and temperature
        weather_condition = current_forecast_data['weather'][0]['main']
        temperature = round(current_forecast_data['main']['temp'])
        iconid = current_forecast_data['weather'][0]['icon']
        icon_url = functions.weather_icon(iconid)

        print(f"DEBUG: Weather condition: {weather_condition}, Temp: {temperature}, Icon: {icon_url}")

        # Fetch Pokémon based on weather
        try:
            pokemon_list = functions.get_types_for_weather(query, weather_condition)
            print(f"DEBUG: Pokémon fetched: {pokemon_list}")  # Log Pokémon list
        except Exception as e:
            print(f"ERROR while fetching Pokémon types: {e}")
            return render_template('results.html', error="Error fetching Pokémon types.")

        # Validate Pokémon data and randomize pairs
        try:
            pokemon_pair_data = functions.randomized_pokemon(pokemon_list)
            print(f"DEBUG: Randomized Pokémon: {pokemon_pair_data}")  # Log randomized Pokémon
        except Exception as e:
            print(f"ERROR while randomizing Pokémon: {e}")
            return render_template('results.html', error="Error processing Pokémon data.")

        # Validate Pokémon pair data structure
        if not isinstance(pokemon_pair_data, list) or not all(
            isinstance(p, dict) and 'name' in p and 'sprite' in p for p in pokemon_pair_data
        ):
            print("ERROR: Invalid Pokémon data structure.")
            return render_template('results.html', error="Invalid Pokémon data received.")

        # Prepare data for the results template
        result_data = {
            "city": query,
            "pokemon": pokemon_pair_data,
            "temperature": temperature,
            "condition": weather_condition,
            "icon": icon_url,
        }
        print(f"DEBUG: Result data prepared: {result_data}")
        return render_template('results.html', data=[result_data])

    except Exception as e:
        # Catch any unexpected errors and log them
        print(f"ERROR in search route: {e}")
        return render_template('results.html', error="An error occurred while processing your request.")


if __name__ == "__main__":
    app.run(debug=True, port=5001)