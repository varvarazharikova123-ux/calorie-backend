from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_views

from foods.views import FoodViewSet
from meals.views import MealViewSet, MealTypeViewSet
from users.views import UserViewSet, ProfileViewSet

# Создаем роутер
router = DefaultRouter()
router.register(r'foods', FoodViewSet, basename='food')
router.register(r'meal-types', MealTypeViewSet, basename='mealtype')
router.register(r'meals', MealViewSet, basename='meal')
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
    path('api/token/', token_views.obtain_auth_token, name='api_token'),
]

# Добавляем медиа файлы в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)