# PokeAPI
# "This is a consumption-only API — only the HTTP GET method is available on resources."

from flask import Flask
import urllib.parse, urllib.request, urllib.error, json
# from geopy.geocoders import Nominatim
import pprint

base_url_pokemon = "https://pokeapi.co/api/v2/"

base_url_weather = "https://api.openweathermap.org/data/3.0/weather"
# https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}

# Some code I had established in an earlier homework (Angel), the understanding of this is to
# pull the info we need from the Pokemon API

def get_pokemon_info(pokemon_name):
    pokemon = f'{base_url_pokemon}pokemon/{pokemon_name.lower()}'

    try:
        print(f'Requesting Pokemon Info: {pokemon}')
        # Did some searching and for some odd reason having this general token helped fix error 403 that I was having
        pokemon_request = urllib.request.Request(pokemon, headers={'User-Agent': 'Mozilla/5.0'})

        with urllib.request.urlopen(pokemon_request) as response:
            pokemon_data = json.loads(response.read().decode('utf-8'))
            # pprint.pprint(pokemon_data)
            pokemon_sprite(pokemon_data)
            return pokemon_data

    except urllib.error.HTTPError as error:
        print("An unexpected error occurred:\nError code: {}".format(error.code))
        return None
    except urllib.error.URLError as error:
        print("The server couldn't fulfill the request.\nError code: {} ".format(error.code))
        return None


def pokemon_sprite(pokemon_data):
    try:
        if pokemon_data and 'sprites' in pokemon_data:
            # Make things simpler I am going to access the default front sprite of the Pokemon
            pokemon_sprite = pokemon_data['sprites']['front_default']
            if pokemon_sprite:
                print(f'Pokemon Sprite Url: {pokemon_sprite}')
            else:
                print('No sprite found for this Pokémon.')
        else:
            print('Invalid pokemon data. No sprite information available.')
    except Exception as error:
        print(f"An error occurred while trying to get Pokemon's sprite: {error}")
        return None


def get_city_data():
    # List of cities and Pokémon
    cities = ["Seattle", "Tacoma", "Vancouver", "Bellingham", "Forks", "Sunnyside"]
    pokemon_list = [
        "Bulbasaur", "Squirtle", "Chikorita","Totodile","Treecko","Mudkip",
        "Turtwig", "Piplup", "Snivy", "Oshawott","Celebi", "Eevee",
    ]

    # Create pairs of Pokémon
    pokemon_pairs = [pokemon_list[i:i + 2] for i in range(0, len(pokemon_list), 2)]

    city_data = []
    for city, pair in zip(cities, pokemon_pairs):
        print(f"DEBUG: Processing city: {city} with Pokémon pair: {pair}")
        pair_data = []
        for pokemon in pair:
            pokemon_info = get_pokemon_info(pokemon)
            if pokemon_info and pokemon_info['sprites']['front_default']:
                pair_data.append({
                    "name": pokemon_info['name'],
                    "sprite": pokemon_info['sprites']['front_default'],
                })
            else:
                print(f"DEBUG: Failed to retrieve data or sprite for Pokémon: {pokemon}")

        if not pair_data:
            print(f"DEBUG: No valid Pokémon data for city: {city}, skipping.")
            continue

        city_data.append({
            "city": city,
            "pokemon": pair_data,  # Add the pair of Pokémon
            "temperature": "44°F",  # Replace with real weather data if desired
            "condition": "Sunny",  # Replace with real weather condition if desired
        })

    print("DEBUG: Current city_data during execution:", city_data)
    return city_data
