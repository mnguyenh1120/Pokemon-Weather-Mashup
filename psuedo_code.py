# PokeAPI
# "This is a consumption-only API — only the HTTP GET method is available on resources."

import urllib.parse, urllib.request, urllib.error, json
import pprint


base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(pokemon_name):
    pokemon = f'{base_url}pokemon/{pokemon_name.lower()}'
    print(f'Requesting Pokemon Info: {pokemon}')

    try:
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

def main():
    # Allows the user to input Pokemon names as many times at they want
    while True:
        pokemon_name = input("Enter the name of Pokemon you wish to search (or 'exit' to quit): ").lower()
        if pokemon_name == 'exit':
            break
        get_pokemon_info(pokemon_name)

main()