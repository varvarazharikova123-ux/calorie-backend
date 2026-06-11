from django.db import models

class Food(models.Model):
    """Модель продукта питания"""
    name = models.CharField(max_length=200, verbose_name='Название')
    barcode = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='Штрихкод')
    
    # Нутриенты на 100г
    calories = models.DecimalField(max_digits=7, decimal_places=1, verbose_name='Калории, ккал')
    protein = models.DecimalField(max_digits=6, decimal_places=1, default=0, verbose_name='Белки, г')
    fat = models.DecimalField(max_digits=6, decimal_places=1, default=0, verbose_name='Жиры, г')
    carbs = models.DecimalField(max_digits=6, decimal_places=1, default=0, verbose_name='Углеводы, г')
    fiber = models.DecimalField(max_digits=6, decimal_places=1, default=0, verbose_name='Клетчатка, г')
    
    image = models.ImageField(upload_to='foods/', null=True, blank=True)
    is_custom = models.BooleanField(default=False, verbose_name='Пользовательский продукт')
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']
    
    def __str__(self):
        return self.name