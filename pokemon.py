import csv
import logging
from typing import List, Tuple

import requests
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
metrics = PrometheusMetrics(app)


def fetch_pokemon_details(limit: int) -> List[Tuple[str, str]]:
    url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}'
    response = requests.get(url)

    try:
        data = response.json()
        pokemon_list = data['results']
        return [(pokemon['name'], pokemon['url']) for pokemon in pokemon_list]
    except (KeyError, TypeError, ValueError) as json_err:
        logging.error(f'JSON parsing error: {json_err}')


def save_queries(pokemon_details: List[Tuple[str, str]], filename: str) -> None:
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "URL"])
            writer.writerows(pokemon_details)
        logging.info(f'Successfully saved queries to {filename}')
    except IOError as io_err:
        logging.error(f'File writing error: {io_err}')


@app.route('/pokemon', methods=['GET'])
def fetch_and_save_pokemon():
    limit = request.args.get('limit', default=10, type=int)
    pokemon_details = fetch_pokemon_details(limit)
    if pokemon_details:
        for name, url in pokemon_details:
            logging.info(f"Name: {name}, URL: {url}")
        save_queries(pokemon_details, 'pokemon_queries.csv')
        return jsonify({"message": "Pokemon details fetched and saved successfully"})
    else:
        logging.error('No Pokemon details retrieved')
        return jsonify({"error": "No Pokemon details retrieved"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
