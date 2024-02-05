from rest_framework.serializers import ModelSerializer
from.models import *


class TestDataSerializer(ModelSerializer):
    class Meta:
        model = CitationLocation
        fields = '__all__'