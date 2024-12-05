# PokeAPI
# "This is a consumption-only API — only the HTTP GET method is available on resources."
# from importlib.metadata import pass_none
from sys import excepthook

import requests
from keys import api_key1
from flask import Flask, current_app
import urllib.parse, urllib.request, urllib.error, json
import pprint
import random
import time

# from matplotlib.sphinxext.mathmpl import latex_math

# https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}

# Some code I had established in an earlier homework (Angel), the understanding of this is to
# pull the info we need from the Pokemon API

weather_to_pokemon_type = {
    "Thunderstorm": ["electric", "flying", "dragon", "water", "bug"],
    "Drizzle": ["water", "bug", "fairy"],
    "Rain": ["water", "electric", "bug"],
    "Snow": ["ice", "steel", "water"],
    "Mist": ["ghost", "dark", "fairy"],
    "Smoke": ["ghost", "dark", "fairy"],
    "Haze": ["ghost", "dark", "fairy"],
    "Dust": ["ghost", "dark", "fairy"],
    "Fog": ["ghost", "dark", "fairy"],
    "Sand": ["ground", "rock", "steel"],
    "Ash": ["fire", "dragon", "flying"],
    "Squall": ["flying", "water", "dragon", "psychic"],
    "Tornado": ["flying", "dragon", "psychic"],
    "Clear": ["fire", "grass", "ground", "normal"],
    "Clouds": ["fairy", "fighting", "poison"],
}

def get_pokemon_info(pokemon_name):
    base_url_pokemon = "https://pokeapi.co/api/v2/"
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


def get_pokemon_by_type(pokemon_types):
    if isinstance(pokemon_types, str):
        pokemon_types = [pokemon_types]
    pokemon_list = []

    for pokemon_type in pokemon_types:
        pokemon_type_url = f'https://pokeapi.co/api/v2/type/{pokemon_type}/'
        pokemon_type_request = urllib.request.Request(pokemon_type_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(pokemon_type_request) as response:
                pokemon_type_data = json.loads(response.read().decode('utf-8'))
                pprint.pprint(pokemon_type_data)
                for pokemon in pokemon_type_data['pokemon']:
                    pokemon_list.append(pokemon['pokemon']['name'])

            time.sleep(1)
        except Exception as error:
            print(f"Error fetching data for type '{pokemon_type}': {error}")
            continue
    print(pokemon_list)
    return pokemon_list

def get_types_for_weather(weather_condition):
    if not weather_condition:
        print("Invalid weather condition received.")
        return None
    print(f'Weather to pull types from : {weather_condition}')
    types_to_search = weather_to_pokemon_type.get(weather_condition)
    if types_to_search:
        pokemon_list = get_pokemon_by_type(types_to_search)
        randomized_pokemon(list(set(pokemon_list)))
    else:
        return None

def randomized_pokemon(pokemon_list):
    shiny_chance = 1 / 4096
    chosen_pokemon = random.choice(pokemon_list)
    is_it_shiny = random.random() < shiny_chance
    return chosen_pokemon, is_it_shiny

def geolocation_finder(location, api_key1, limit = 1):
    base_url_geolocation = "http://api.openweathermap.org/geo/1.0/direct?q="
    geolocation = f'{base_url_geolocation}{location}&limit={limit}&appid={api_key1}'

    geolocation_request = urllib.request.Request(geolocation)

    with urllib.request.urlopen(geolocation_request) as response:
        location_data = json.loads(response.read().decode('utf-8'))
        # pprint.pprint(location_data)
        if location_data:
            coordinates = (location_data[0]['lat'], location_data[0]['lon'])
            get_current_forecast(coordinates, api_key1)
            return coordinates
        else:
            return None

def get_current_forecast(coordinates, api_key1):
    if not coordinates:
        return None
    try:
        base_url_weather = "https://api.openweathermap.org/data/2.5/weather?"
        current_forecast = f'{base_url_weather}lat={coordinates[0]}&lon={coordinates[1]}&appid={api_key1}'
        print(f"Request URL: {current_forecast}")
        current_forecast_request = urllib.request.Request(current_forecast)

        with urllib.request.urlopen(current_forecast_request) as response:
            current_forecast_data = json.loads(response.read().decode('utf-8'))
            pprint.pprint(current_forecast_data)
            if current_forecast_data:
                weather_condition = current_forecast_data['weather'][0]['main']
                iconid = current_forecast_data['weather'][0]['icon']
                weather_icon(iconid)
                print(f'Current Forecast: {weather_condition}')
                get_types_for_weather(weather_condition)
            else:
                return None

    except Exception as error:
        print(f"An error occurred while trying to get current weather forecast: {error}")

def weather_icon(iconid):
    icon_url = f'https://openweathermap.org/img/wn/{iconid}.png'
    print(f"Request URL: {icon_url}")
    # icon_url_doubled = f'https://openweathermap.org/img/wn/{iconid}@2x.png'


geolocation_finder('Seattle', api_key1)
# get_types_for_weather("Rain")
# get_pokemon_by_type('fire')