# PokeAPI
# "This is a consumption-only API — only the HTTP GET method is available on resources."

from flask import Flask
import urllib.parse, urllib.request, urllib.error, json
# from geopy.geocoders import Nominatim
import pprint

base_url_pokemon = "https://pokeapi.co/api/v2/"

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
            return pokemon_data #

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

# pokemon_name = 'pikachu' # Passes, no changes needed
# get_pokemon_info(pokemon_name)
# pokemon_name = 'Pikachu' # Also passes, ensure that as long as the name is spelt correctly it gives the correct info as it's automatically lowercased
# get_pokemon_info(pokemon_name)
# pokemon_name = 'Pikachuu' # Fails, error code 404 since it is not spelt correctly
# get_pokemon_info(pokemon_name)

# Function to get the Pokemon's habitat
    # Can be called from get_pokemon_info
    # returns habitat from pokemon_data

# Function to get the Pokemon's type
    # Can be called from get_pokemon_info
    # returns type from pokemon_data

# Function to get the

def main():
    # Allows the user to input Pokemon names as many times at they want
    while True:
        pokemon_name = input("Enter the name of Pokemon you wish to search (or 'exit' to quit): ").lower()
        if pokemon_name == 'exit':
            break
        get_pokemon_info(pokemon_name)

# main()
basic_weather_conditions = {
  "clear": ["Fire", "Grass", "Ground"],
  "rain": ["Water", "Electric", "Bug"],
  "snow": ["Ice", "Steel"],
  "wind": ["Flying", "Dragon", "Psychic"],
  "clouds": ["Fairy", "Fighting", "Poison"],
  "fog": ["Ghost", "Dark"]
}

# Pseudo Code for Weather API
# base_url_weather = "https://api.openweathermap.org/data/3.0/weather"
# https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}

# Function that calls geopy takes in the name of the area
    # returns the lat and lng for the weather API

# Function that calls current predetermined locations in Washington
    # Code that runs within it and calls the get_pokemon_info

# Function that considers optional locations for current weather locations
    # Takes the lat and lng of the geopy function

# Function that takes the current weather conditions as a parameter
    # Create a randomness variable assigned to each pokemon on that list
    # Chooses two pokemon from a list of pokemon that appear during that weather, based on highest value
    # returns the two pokemon which will be used to get the sprite to add to the card shown on the readme
