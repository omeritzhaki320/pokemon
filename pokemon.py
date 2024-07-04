import csv
import logging

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_pokemon_details(limit: int) -> list[tuple[str, str]]:
    """
    Fetches Pokemon details from the PokeAPI.
    :param limit: number of Pokemon to fetch
    """
    url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}'
    response = requests.get(url)

    try:
        data = response.json()
        pokemon_list = data['results']
        return [(pokemon['name'], pokemon['url']) for pokemon in pokemon_list]
    except (KeyError, TypeError, ValueError) as json_err:
        logging.error(f'JSON parsing error: {json_err}')


def save_queries(pokemon_details: list[tuple[str, str]], filename: str) -> None:
    """
    Saves user queries to a CSV file.
    :param pokemon_details: tuple of (name, url)
    :param filename: the filename to save to
    """
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "URL"])  # Write the header
            writer.writerows(pokemon_details)  # Write the pokemon details
        logging.info(f'Successfully saved queries to {filename}')
    except IOError as io_err:
        logging.error(f'File writing error: {io_err}')
        print(f'File writing error: {io_err}')


def main():
    queries_file_name = 'pokemon_queries.csv'
    pokemon_details = fetch_pokemon_details(10)

    if pokemon_details:
        for name, url in pokemon_details:
            logging.info(f"Name: {name}, URL: {url}")
        save_queries(pokemon_details, queries_file_name)
    else:
        logging.error('No Pokemon details retrieved')


if __name__ == '__main__':
    main()
