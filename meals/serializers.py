from rest_framework import serializers
from .models import Meal, MealItem, MealType
from foods.serializers import FoodSerializer

class MealItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    food_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = MealItem
        fields = ['id', 'food', 'food_id', 'quantity', 'unit', 'calories', 'protein', 'fat', 'carbs']

class MealSerializer(serializers.ModelSerializer):
    items = MealItemSerializer(many=True, read_only=True)
    meal_type_name = serializers.CharField(source='meal_type.name', read_only=True)
    meal_type_icon = serializers.CharField(source='meal_type.icon', read_only=True)
    total_calories = serializers.SerializerMethodField()
    total_protein = serializers.SerializerMethodField()
    total_fat = serializers.SerializerMethodField()
    total_carbs = serializers.SerializerMethodField()
    
    class Meta:
        model = Meal
        fields = ['id', 'meal_type', 'meal_type_name', 'meal_type_icon', 'date', 'items', 
                  'total_calories', 'total_protein', 'total_fat', 'total_carbs']
    
    def get_total_calories(self, obj):
        return obj.total_calories()
    
    def get_total_protein(self, obj):
        return obj.total_protein()
    
    def get_total_fat(self, obj):
        return obj.total_fat()
    
    def get_total_carbs(self, obj):
        return obj.total_carbs()

class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = ['id', 'name', 'icon', 'order']