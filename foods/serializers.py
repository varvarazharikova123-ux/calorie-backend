from rest_framework import serializers
from .models import Food

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'barcode', 'calories', 'protein', 'fat', 'carbs', 'fiber', 'image', 'is_custom']

class FoodSearchSerializer(serializers.Serializer):
    query = serializers.CharField()
    limit = serializers.IntegerField(default=20)