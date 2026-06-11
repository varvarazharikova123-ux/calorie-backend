from django.contrib import admin
from .models import MealType, Meal, MealItem

@admin.register(MealType)
class MealTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order')
    list_editable = ('order',)

class MealItemInline(admin.TabularInline):
    model = MealItem
    extra = 1

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_type', 'date', 'total_calories')
    list_filter = ('date', 'meal_type')
    inlines = [MealItemInline]
    
    def total_calories(self, obj):
        return obj.total_calories()
    total_calories.short_description = 'Калории'

@admin.register(MealItem)
class MealItemAdmin(admin.ModelAdmin):
    list_display = ('meal', 'food', 'quantity', 'unit', 'calories')