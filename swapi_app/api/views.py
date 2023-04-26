import os

import petl as etl
from petl.errors import FieldSelectionError

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from swapi_app import tasks
from swapi_app.models import MetaData
from .serializers import CharacterSerializer, DictsSerializer, MetadataSerializer

from swapi_project import settings



@api_view(["GET"])
def dataset_metadata_list(request):
    metadata = MetaData.objects.all()
    serializer = MetadataSerializer(metadata, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
def fetch_and_process_data(request):
    tasks.fetch_data()  # Assuming the task function is in the tasks.py file
    return JsonResponse({"status": "success"})


@api_view(["GET"])
def get_dataset_data(request, metadata_id, page):
    metadata = get_object_or_404(MetaData, id=metadata_id)

    table = etl.empty()

    filename_prefix = f"{metadata_id}_"

    filename = f"{filename_prefix}{page}.csv"
    filepath = os.path.join(settings.BASE_DIR, "media", "datasets", filename)

    # Check if the file exists before attempting to read it
    if os.path.exists(filepath):
        file_table = etl.fromcsv(filepath)
        table = etl.cat(table, file_table)
    else:
        # TODO: Logger Implementation and logging.
        pass

    # Serialize the data using CharacterSerializer
    data = etl.dicts(table)
    serializer = CharacterSerializer(data, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def value_count(request, metadata_id, columns):
    metadata = get_object_or_404(MetaData, id=metadata_id)
    table = etl.empty()

    columns = columns.split(",")
    filename_prefix = f"{metadata_id}_"

    for i in range(metadata.num_files):
        filename = f"{filename_prefix}{i + 1}.csv"
        filepath = os.path.join(settings.BASE_DIR, "media", "datasets", filename)

        try:
            file_table = etl.fromcsv(filepath)
        except FileNotFoundError:
            continue

        table = etl.cat(table, file_table)

    try:
        table = etl.aggregate(table, key=columns, aggregation=len)
        # Serialize the data using CharacterSerializer
        data = etl.dicts(table)
        serializer = DictsSerializer(data={"data": data})
        serializer.is_valid()
        return Response(serializer.data)

    except FieldSelectionError as e:
        raise ValidationError("Invalid Column Specified: %s" % (e.value))
