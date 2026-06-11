from django.db import models
from django.core.validators import MinValueValidator

class MealType(models.Model):
    """Тип приема пищи"""
    name = models.CharField(max_length=50, verbose_name='Название')
    icon = models.CharField(max_length=50, default='restaurant', verbose_name='Иконка')
    order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Тип приема пищи'
        verbose_name_plural = 'Типы приемов пищи'
    
    def __str__(self):
        return self.name

class Meal(models.Model):
    """Прием пищи за день"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='meals', null=True, blank=True)
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE, related_name='meals')
    date = models.DateField(verbose_name='Дата')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'meal_type', 'date']
        ordering = ['-date', 'meal_type__order']
        verbose_name = 'Прием пищи'
        verbose_name_plural = 'Приемы пищи'
    
    def total_calories(self):
        return sum(item.calories for item in self.items.all())
    
    def total_protein(self):
        return sum(item.protein for item in self.items.all())
    
    def total_fat(self):
        return sum(item.fat for item in self.items.all())
    
    def total_carbs(self):
        return sum(item.carbs for item in self.items.all())

class MealItem(models.Model):
    """Позиция в приеме пищи"""
    UNIT_CHOICES = [
        ('g', 'грамм'),
        ('ml', 'миллилитр'),
        ('pcs', 'штук'),
    ]
    
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey('foods.Food', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=7, decimal_places=1, validators=[MinValueValidator(0.1)])
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES, default='g')
    
    # Кэшированные значения
    calories = models.DecimalField(max_digits=7, decimal_places=1, default=0)
    protein = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    fat = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    carbs = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Расчет нутриентов на основе порции
        factor = float(self.quantity) / 100
        self.calories = float(self.food.calories) * factor
        self.protein = float(self.food.protein) * factor
        self.fat = float(self.food.fat) * factor
        self.carbs = float(self.food.carbs) * factor
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quantity}{self.unit} {self.food.name}"