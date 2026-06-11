from rest_framework import serializers
from .models import Diet, DailyMealPlan, Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class DailyMealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMealPlan
        fields = '__all__'

class DietSerializer(serializers.ModelSerializer):
    daily_plans = DailyMealPlanSerializer(many=True, read_only=True)
    recipes = RecipeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Diet
        fields = '__all__'