import csv
import logging
from typing import List, Tuple

import requests
import uvicorn
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()


def fetch_pokemon_details(limit: int) -> List[Tuple[str, str]]:
    url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}'
    response = requests.get(url)

    try:
        data = response.json()
        pokemon_list = data['results']
        return [(pokemon['name'], pokemon['url']) for pokemon in pokemon_list]
    except (KeyError, TypeError, ValueError) as json_err:
        logging.error(f'JSON parsing error: {json_err}')
        raise HTTPException(status_code=500, detail="Error fetching Pokemon details")


def save_queries(pokemon_details: List[Tuple[str, str]], filename: str) -> None:
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "URL"])
            writer.writerows(pokemon_details)
        logging.info(f'Successfully saved queries to {filename}')
    except IOError as io_err:
        logging.error(f'File writing error: {io_err}')
        raise HTTPException(status_code=500, detail="Error saving Pokemon details")


@app.get("/pokemon")
def fetch_and_save_pokemon(limit: int = 10):
    pokemon_details = fetch_pokemon_details(limit)
    if pokemon_details:
        for name, url in pokemon_details:
            logging.info(f"Name: {name}, URL: {url}")
        save_queries(pokemon_details, 'pokemon_queries.csv')
        return {"message": "Pokemon details fetched and saved successfully"}
    else:
        logging.error('No Pokemon details retrieved')
        raise HTTPException(status_code=404, detail="No Pokemon details retrieved")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
