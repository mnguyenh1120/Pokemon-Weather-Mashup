import experiment
import functions
from flask import Flask, render_template, request
import urllib.parse, urllib.request, urllib.error, json
# from geopy.geocoders import Nominatim
import pprint

# Create an instance of Flask
app = Flask(__name__)

@app.route('/')
def home():
    data = experiment.get_city_data()
    print("DEBUG: Data returned by get_city_data:", data)  # Debugging line
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/results", methods=["GET"])
# def results():
#     pokemon_name = request.args.get("pokemon_name")
#
#     if not pokemon_name:
#         return "<h1>Error: Not a Pokémon name provided</h1>"
#
#     # Fetch Pokémon data using your functions.py
#     pokemon_data = functions.get_pokemon_info(pokemon_name)
#
#     if not pokemon_data:
#         return f"<h1>Sorry, no data found for Pokémon: {pokemon_name}</h1>"
#
#     # Construct an HTML response dynamically
#     response = f"""
#         <h1>Pokémon Information</h1>
#         <p>Name: {pokemon_data['name'].capitalize()}</p>
#         <img src="{pokemon_data['sprites']['front_default']}" alt="Pokémon Sprite">
#         <br><a href="/">Go back</a>
#     """
#     return response
#
# if __name__ == "__main__":
#     app.run(debug=True)