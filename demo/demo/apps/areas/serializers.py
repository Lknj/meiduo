from rest_framework import serializers
from .models import AreaInfo


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaInfo
        fields = ['id', 'name']


class SubAreaSerializer(serializers.ModelSerializer):
    subs = AreaSerializer(read_only=True, many=True)
    class Meta:
        model = AreaInfo
        fields = ['id', 'name', 'subs']
