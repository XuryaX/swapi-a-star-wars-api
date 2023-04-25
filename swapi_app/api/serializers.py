from rest_framework import serializers
from swapi_app.models import DatasetMetadata

class DatasetMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetMetadata
        fields = '__all__'
