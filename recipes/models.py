from django.db import models
from django.utils import timezone

class Diet(models.Model):
    """Модель диеты"""
    name = models.CharField(max_length=100, verbose_name='Название')
    icon = models.CharField(max_length=10, default='🥗', verbose_name='Иконка')
    description = models.TextField(verbose_name='Описание')
    duration_days = models.IntegerField(default=7, verbose_name='Длительность (дней)')
    calories_range = models.CharField(max_length=50, verbose_name='Диапазон калорий')
    color = models.CharField(max_length=20, default='#FF6B35', verbose_name='Цвет')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    
    class Meta:
        verbose_name = 'Диета'
        verbose_name_plural = 'Диеты'
    
    def __str__(self):
        return self.name

class DailyMealPlan(models.Model):
    """Дневной план питания для диеты"""
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, related_name='daily_plans')
    day_number = models.PositiveIntegerField(verbose_name='День')
    breakfast = models.TextField(verbose_name='Завтрак')
    lunch = models.TextField(verbose_name='Обед')
    dinner = models.TextField(verbose_name='Ужин')
    snack = models.TextField(verbose_name='Перекус', blank=True)
    
    class Meta:
        unique_together = ['diet', 'day_number']
        ordering = ['day_number']
        verbose_name = 'Дневной план'
        verbose_name_plural = 'Дневные планы'
    
    def __str__(self):
        return f"{self.diet.name} - День {self.day_number}"

class Recipe(models.Model):
    """Модель рецепта"""
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ('snack', 'Перекус'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    ingredients = models.TextField(verbose_name='Ингредиенты')
    instructions = models.TextField(verbose_name='Приготовление')
    prep_time = models.PositiveIntegerField(default=30, verbose_name='Время приготовления (мин)')
    calories = models.PositiveIntegerField(default=0, verbose_name='Калории')
    protein = models.PositiveIntegerField(default=0, verbose_name='Белки')
    fat = models.PositiveIntegerField(default=0, verbose_name='Жиры')
    carbs = models.PositiveIntegerField(default=0, verbose_name='Углеводы')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, verbose_name='Тип приема')
    image_url = models.URLField(blank=True, null=True, verbose_name='URL изображения')
    video_url = models.URLField(blank=True, null=True, verbose_name='URL видео')
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, related_name='recipes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    
    def __str__(self):
        return self.name