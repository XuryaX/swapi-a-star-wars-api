# tasks.py
import petl as etl
import requests
import csv
import os
from swapi_project import settings
from .models import MetaData


def fetch_characters():
    url = "https://swapi.co/api/people/"
    characters = []

    while url:
        response = requests.get(url)
        data = response.json()
        characters.extend(data["results"])
        url = data["next"]

    return characters


def process_characters(characters):
    table = etl.fromdicts(characters)
    table = etl.addfield(table, "date", lambda row: row["edited"].split("T")[0])
    table = etl.convert(table, "homeworld", lambda url: requests.get(url).json()["name"])

    fields_to_keep = ["name", "height", "mass", "hair_color", "skin_color", "eye_color", "birth_year", "gender", "homeworld", "date"]
    table = etl.cut(table, *fields_to_keep)

    return table



def save_data_to_csv(table, metadata):
    num_files = -(-len(table) // settings.ROWS_PER_FILE)  # Ceiling division
    filename_prefix = f"swapi_data_{metadata.id}_"

    for i in range(num_files):
        start = i * settings.ROWS_PER_FILE
        end = start + settings.ROWS_PER_FILE
        file_table = etl.rowlenseslice(table, start, end)
        filename = f"{filename_prefix}{i + 1}.csv"
        filepath = os.path.join(settings.BASE_DIR, "data", filename)

        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            etl.tocsv(file_table, csvfile)

    metadata.filename_prefix = filename_prefix
    metadata.num_files = num_files
    metadata.save()


def fetch_data():
    characters = fetch_characters()
    processed_data = process_characters(characters)
    metadata = MetaData.objects.create()

    save_data_to_csv(processed_data, metadata)
