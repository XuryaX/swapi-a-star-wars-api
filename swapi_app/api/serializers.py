from rest_framework import serializers
from swapi_app.models import MetaData

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        fields = '__all__'

class CharacterSerializer(serializers.Serializer):
    name = serializers.CharField()
    height = serializers.CharField()
    mass = serializers.CharField()
    hair_color = serializers.CharField()
    skin_color = serializers.CharField()
    eye_color = serializers.CharField()
    birth_year = serializers.CharField()
    gender = serializers.CharField()
    homeworld = serializers.CharField()
    date = serializers.CharField()


class DictsSerializer(serializers.Serializer):
    data = serializers.ListField(child=serializers.DictField())
