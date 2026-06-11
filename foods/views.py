from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Food
from .serializers import FoodSerializer

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        limit = int(request.query_params.get('limit', 20))
        
        foods = Food.objects.filter(
            Q(name__icontains=query) | Q(barcode=query)
        )[:limit]
        
        serializer = self.get_serializer(foods, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_barcode(self, request):
        barcode = request.query_params.get('barcode')
        if not barcode:
            return Response({'error': 'Barcode required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            food = Food.objects.get(barcode=barcode)
            serializer = self.get_serializer(food)
            return Response(serializer.data)
        except Food.DoesNotExist:
            return Response({'error': 'Food not found'}, status=status.HTTP_404_NOT_FOUND)