import petl as etl
import requests
import csv
import os
from swapi_project import settings
from .models import MetaData
from .cache import InMemoryCache

cache = InMemoryCache()


def fetch_characters():
    url = "https://swapi.dev/api/people/"
    characters = []

    while url:
        response = requests.get(url)
        data = response.json()
        characters.extend(data["results"])
        url = data["next"]

    return characters

def fetch_homeworld_name(url):
    if cache.has(url):
        return cache.get(url)
    else:
        name = requests.get(url).json()["name"]
        cache.set(url, name)
        return name


def process_characters(characters):
    table = etl.fromdicts(characters)
    table = etl.addfield(table, "date", lambda row: row["edited"].split("T")[0])
    table = etl.convert(table, "homeworld", fetch_homeworld_name)

    fields_to_keep = ["name", "height", "mass", "hair_color", "skin_color", "eye_color", "birth_year", "gender", "homeworld", "date"]
    table = etl.cut(table, *fields_to_keep)

    return table, len(characters)



def save_data_to_csv(table, table_length):
    num_files = -(-table_length // settings.ROWS_PER_FILE)  # Ceiling division

    # Create MetaData object with num_files value
    metadata = MetaData.objects.create(num_files=num_files)
    filename_prefix = f"{metadata.id}_"

    for i in range(num_files):
        start = i * settings.ROWS_PER_FILE
        end = start + settings.ROWS_PER_FILE

        file_table = etl.rowslice(table, start, end)

        filename = f"{filename_prefix}{i + 1}.csv"

        filepath = os.path.join(settings.BASE_DIR, "media", "datasets", filename)

        # Create the media/datasets directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        etl.tocsv(file_table, filepath, encoding="utf-8")

    metadata.save()


def fetch_data():
    characters = fetch_characters()
    
    processed_data, table_length = process_characters(characters)
    save_data_to_csv(processed_data, table_length)
