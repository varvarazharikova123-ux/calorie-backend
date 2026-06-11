from django.contrib import admin
from .models import Diet, DailyMealPlan, Recipe

@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_days', 'calories_range', 'is_active')

@admin.register(DailyMealPlan)
class DailyMealPlanAdmin(admin.ModelAdmin):
    list_display = ('diet', 'day_number')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'meal_type', 'calories', 'prep_time')
    list_filter = ('meal_type', 'diet')
    search_fields = ('name',)