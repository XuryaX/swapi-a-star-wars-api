from django.http import JsonResponse
from rest_framework.decorators import api_view
from swapi_app.models import DatasetMetadata
from swapi_app.tasks import read_data_from_csv
from swapi_app import tasks
from .serializers import DatasetMetadataSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import petl as etl
from swapi_project import settings
from .models import MetaData


@api_view(["GET"])
def dataset_metadata_list(request):
    metadata = DatasetMetadata.objects.all()
    serializer = DatasetMetadataSerializer(metadata, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
def fetch_and_process_data(request):
    tasks.fetch_data()  # Assuming the task function is in the tasks.py file
    return JsonResponse({"status": "success"})


@api_view(["GET"])
def get_dataset_data(request, metadata_id, page):
    metadata = MetaData.objects.get(id=metadata_id)
    start_file = (page - 1) * settings.FILES_PER_PAGE
    end_file = start_file + settings.FILES_PER_PAGE
    table = etl.empty()

    for i in range(start_file, min(end_file, metadata.num_files)):
        filename = f"{metadata.filename_prefix}{i + 1}.csv"
        filepath = os.path.join(settings.BASE_DIR, "data", filename)
        file_table = etl.fromcsv(filepath)
        table = etl.cat(table, file_table)

    return Response(etl.dicts(table))


@api_view(["GET"])
def value_count(request, metadata_id, columns):
    metadata = MetaData.objects.get(id=metadata_id)
    table = etl.empty()

    columns = columns.split(",")

    for i in range(metadata.num_files):
        filename = f"{metadata.filename_prefix}{i + 1}.csv"
        filepath = os.path.join(settings.BASE_DIR, "data", filename)
        file_table = etl.fromcsv(filepath)
        table = etl.cat(table, file_table)

    table = etl.aggregate(table, key=columns, aggregation=len)
    return Response(etl.dicts(table))
