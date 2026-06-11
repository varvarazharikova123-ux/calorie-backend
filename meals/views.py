from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import datetime
from .models import Meal, MealItem, MealType
from .serializers import MealSerializer, MealItemSerializer, MealTypeSerializer

class MealTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MealType.objects.all()
    serializer_class = MealTypeSerializer
    permission_classes = [AllowAny]

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        meals = Meal.objects.filter(date=today)
        serializer = self.get_serializer(meals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_date(self, request):
        date_str = request.query_params.get('date')
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = timezone.now().date()
        
        meals = Meal.objects.filter(date=date)
        serializer = self.get_serializer(meals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        date_str = request.query_params.get('date')
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = timezone.now().date()
        
        meals = Meal.objects.filter(date=date)
        
        total_calories = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0
        
        for meal in meals:
            total_calories += meal.total_calories()
            total_protein += meal.total_protein()
            total_fat += meal.total_fat()
            total_carbs += meal.total_carbs()
        
        data = {
            'date': date,
            'total_calories': total_calories,
            'total_protein': total_protein,
            'total_fat': total_fat,
            'total_carbs': total_carbs,
            'water_ml': 0,
            'meals': MealSerializer(meals, many=True).data
        }
        
        return Response(data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        meal_id = request.data.get('meal_id')
        food_id = request.data.get('food_id')
        quantity = request.data.get('quantity')
        unit = request.data.get('unit', 'g')
        
        try:
            meal = Meal.objects.get(id=meal_id)
            meal_item = MealItem.objects.create(
                meal=meal,
                food_id=food_id,
                quantity=quantity,
                unit=unit
            )
            # Обновляем прием пищи
            meal.save()
            serializer = MealItemSerializer(meal_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Meal.DoesNotExist:
            return Response({'error': 'Meal not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        item_id = request.query_params.get('item_id')
        try:
            item = MealItem.objects.get(id=item_id)
            item.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except MealItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)