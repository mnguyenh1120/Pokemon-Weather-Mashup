# PokeAPI
# "This is a consumption-only API — only the HTTP GET method is available on resources."
# from importlib.metadata import pass_none

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

base_url_pokemon = "https://pokeapi.co/api/v2/"
pokemon_cache = {}
CACHE_EXPIRE_TIME = 600

def is_cache_expired(city, weather_condition):
    key = (city, weather_condition)
    if key not in pokemon_cache:
        return True
    cache_time = pokemon_cache[key]['timestamp']
    return CACHE_EXPIRE_TIME > (time.time() - cache_time)

def pokemon_sprite(pokemon_data, shiny_status):
    try:
        if pokemon_data and 'sprites' in pokemon_data:
            # Make things simpler I am going to access the default front sprite of the Pokemon
            if shiny_status:
                pokemon_sprite = pokemon_data['sprites']['front_shiny']
            else:
                pokemon_sprite = pokemon_data['sprites']['front_default']

            # Incase it is an alternate version of that specific pokemon that does not have a sprite
            if not pokemon_sprite and 'species' in pokemon_data:
                print(f"No sprite found for {pokemon_data['species']['name']} due to alternate version not having a sprite")
                species_name = pokemon_data['species']['name']
                species_url = f'{base_url_pokemon}pokemon/{species_name}'
                species_request = urllib.request.Request(species_url, headers={'User-Agent': 'Mozilla/5.0'})
                try:
                    with urllib.request.urlopen(species_request) as response:
                        species_data = json.loads(response.read().decode('utf-8'))
                        if shiny_status:
                            pokemon_sprite = species_data['sprites']['front_shiny']
                        else:
                            pokemon_sprite = species_data['sprites']['front_default']

                except urllib.error.HTTPError as error:
                    print("An unexpected error occurred:\nError code: {}".format(error.code))
                    return None
                except urllib.error.URLError as error:
                    print("The server couldn't fulfill the request.\nError code: {} ".format(error.code))
                    return None

            if pokemon_sprite:
                print(f'Pokemon Sprite Url: {pokemon_sprite}')
            else:
                print('No sprite found for this Pokémon.')
            return pokemon_sprite
        else:
            print('Invalid pokemon data. No sprite information available.')
    except Exception as error:
        print(f"An error occurred while trying to get Pokemon's sprite: {error}")
        return None

def get_pokemon_info(pokemon_name, shiny_status):
    pokemon = f'{base_url_pokemon}pokemon/{pokemon_name.lower()}'

    try:
        print(f'Requesting Pokemon Info: {pokemon}')
        # Did some searching and for some odd reason having this general token helped fix error 403 that I was having
        pokemon_request = urllib.request.Request(pokemon, headers={'User-Agent': 'Mozilla/5.0'})

        with urllib.request.urlopen(pokemon_request) as response:
            pokemon_data = json.loads(response.read().decode('utf-8'))
            # pprint.pprint(pokemon_data)
        sprite_url = pokemon_sprite(pokemon_data, shiny_status)

        return sprite_url

    except urllib.error.HTTPError as error:
        print("An unexpected error occurred:\nError code: {}".format(error.code))
        return None
    except urllib.error.URLError as error:
        print("The server couldn't fulfill the request.\nError code: {} ".format(error.code))
        return None

def get_pokemon_by_type(pokemon_types):
    pokemon_list = []
    if isinstance(pokemon_types, str):
        pokemon_types = [pokemon_types]

    for pokemon_type in pokemon_types:
        pokemon_type_url = f'https://pokeapi.co/api/v2/type/{pokemon_type}/'
        pokemon_type_request = urllib.request.Request(pokemon_type_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(pokemon_type_request) as response:
                pokemon_type_data = json.loads(response.read().decode('utf-8'))
                # pprint.pprint(pokemon_type_data)
                for pokemon in pokemon_type_data['pokemon']:
                    pokemon_list.append(pokemon['pokemon']['name'])
            time.sleep(0.25)

        except Exception as error:
            print(f"Error fetching data for type '{pokemon_type}': {error}")
            continue
    # print(pokemon_list)
    return pokemon_list

def randomized_pokemon(pokemon_list):
    shiny_chance = 1 / 4096
    number_of_pokemon = 2
    pokemon_pair_data = []

    chosen_pokemon = random.sample(pokemon_list, number_of_pokemon)
    shiny_status = [random.random() < shiny_chance for assigned_pokemon in chosen_pokemon]
    pair_pokemon_status = [(pokemon, is_shiny) for pokemon, is_shiny in zip(chosen_pokemon, shiny_status)]
    for pokemon, shiny_status in pair_pokemon_status:
        pokemon_sprite = get_pokemon_info(pokemon, shiny_status)
        pokemon_pair_data.append({
            'name': pokemon,
            'sprite': pokemon_sprite
        })
    return pokemon_pair_data

def get_types_for_weather(city, weather_condition):
    ### Implementing a cache system ###
    key = (city, weather_condition)
    if key in pokemon_cache and is_cache_expired(city, weather_condition):
        print(f"Using cached data for {city}, {weather_condition}")
        return pokemon_cache[key]['pokemon_data']

    if not weather_condition:
        print("Invalid weather condition received.")
        return None
    print(f'Weather to pull types from : {weather_condition}')
    types_to_search = weather_to_pokemon_type.get(weather_condition)
    if types_to_search:
        pokemon_list = get_pokemon_by_type(types_to_search)
        # randomized_pokemon(list(set(pokemon_list)))
        pokemon_pair_data = randomized_pokemon(pokemon_list)
        ### Stores the cache with pokemons ###
        pokemon_cache[key] = {
            'pokemon_data': list(pokemon_pair_data),
            'timestamp': time.time()
        }
        return pokemon_pair_data
    else:
        return None

def geolocation_finder(location, api_key1, limit = 1):
    base_url_geolocation = "http://api.openweathermap.org/geo/1.0/direct?q="
    if ' ' in location:
        location = urllib.parse.quote(location)
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
        current_forecast = f'{base_url_weather}lat={coordinates[0]}&lon={coordinates[1]}&appid={api_key1}&units=imperial'
        # print(f"Request URL: {current_forecast}")
        current_forecast_request = urllib.request.Request(current_forecast)

        with urllib.request.urlopen(current_forecast_request) as response:
            current_forecast_data = json.loads(response.read().decode('utf-8'))
            # pprint.pprint(current_forecast_data)
            if current_forecast_data:
                return current_forecast_data
            else:
                return None

    except Exception as error:
        print(f"An error occurred while trying to get current weather forecast: {error}")

def weather_icon(iconid):
    icon_url = f'https://openweathermap.org/img/wn/{iconid}.png'
    # print(f"Request URL: {icon_url}")
    # icon_url_doubled = f'https://openweathermap.org/img/wn/{iconid}@2x.png'
    return icon_url

def get_city_data(query=None):
    city_data = []
    cities = []
    if query:
        cities = [city.strip() for city in query.split(',')]
    else:
        cities = ["Seattle", "Tacoma", "Vancouver", "Bellingham", "Forks", "Sunnyside", "Olympia", "Yakima", "Kennewick"]
    for city in cities:
        coordinates = geolocation_finder(city, api_key1)
        current_forecast_data = get_current_forecast(coordinates, api_key1)
        weather_condition = current_forecast_data['weather'][0]['main']
        iconid = current_forecast_data['weather'][0]['icon']
        temperature = round(current_forecast_data['main']['temp'])
        icon_url = weather_icon(iconid)
        # print(f'Current Forecast: {weather_condition}')
        pokemon_pair_data = get_types_for_weather(city, weather_condition)
        city_data.append({
            "city": city,
            "pokemon": pokemon_pair_data,  # Add the pair of Pokémon
            "temperature": temperature,  # Replace with real weather data if desired
            "condition": weather_condition,
            "icon": icon_url # Replace with real weather condition if desired)
        })
    # time.sleep(0.25)
    return city_data


#geolocation_finder('Seattle', api_key1)
# get_types_for_weather("Rain")
# get_pokemon_by_type('fire')
# get_city_data()
# time.sleep(5)
# get_city_data()