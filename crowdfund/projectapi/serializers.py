from rest_framework import serializers
from projects.models import Project


class Projectser(serializers.ModelSerializer):
    extra_images = serializers.StringRelatedField(many=True)
    class Meta:
        model = Project
        fields = '__all__'