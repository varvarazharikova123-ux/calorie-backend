from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import Diet, DailyMealPlan, Recipe
from .serializers import DietSerializer, DailyMealPlanSerializer, RecipeSerializer

class DietViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Diet.objects.filter(is_active=True)
    serializer_class = DietSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def todays_plan(self, request):
        """Получить план питания на сегодня"""
        diet_id = request.query_params.get('diet_id')
        if not diet_id:
            return Response({'error': 'diet_id required'}, status=400)
        
        try:
            diet = Diet.objects.get(id=diet_id)
            # Рассчитываем день диеты на основе даты начала (в реальном приложении нужно хранить дату начала)
            # Для демо используем фиксированный день
            day_number = (datetime.now().day % diet.duration_days) + 1
            daily_plan = DailyMealPlan.objects.get(diet=diet, day_number=day_number)
            serializer = DailyMealPlanSerializer(daily_plan)
            return Response(serializer.data)
        except Diet.DoesNotExist:
            return Response({'error': 'Diet not found'}, status=404)
        except DailyMealPlan.DoesNotExist:
            return Response({'error': 'Plan not found'}, status=404)
    
    @action(detail=False, methods=['get'])
    def random_recipe(self, request):
        """Получить случайный рецепт"""
        diet_id = request.query_params.get('diet_id')
        queryset = Recipe.objects.all()
        if diet_id:
            queryset = queryset.filter(diet_id=diet_id)
        
        recipe = queryset.order_by('?').first()
        if recipe:
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data)
        return Response({'error': 'No recipes found'}, status=404)

class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        meal_type = request.query_params.get('meal_type', '')
        
        recipes = Recipe.objects.all()
        if query:
            recipes = recipes.filter(name__icontains=query)
        if meal_type:
            recipes = recipes.filter(meal_type=meal_type)
        
        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)