from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Расширенная модель пользователя"""
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Добавляем related_name для избежания конфликтов
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    
    def __str__(self):
        return self.username

class Profile(models.Model):
    """Профиль с антропометрическими данными"""
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    ACTIVITY_CHOICES = [
        (1.2, 'Сидячий образ жизни'),
        (1.375, 'Легкая активность (1-3 раза/нед)'),
        (1.55, 'Средняя активность (3-5 раз/нед)'),
        (1.725, 'Высокая активность (6-7 раз/нед)'),
        (1.9, 'Очень высокая активность (2 раза/день)'),
    ]
    
    GOAL_CHOICES = [
        ('lose', 'Похудение'),
        ('maintain', 'Поддержание'),
        ('gain', 'Набор массы'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    height = models.PositiveIntegerField(help_text='Рост в см')
    weight = models.DecimalField(max_digits=5, decimal_places=1, help_text='Вес в кг')
    activity_level = models.DecimalField(max_digits=4, decimal_places=3, choices=ACTIVITY_CHOICES)
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES)
    daily_calorie_goal = models.PositiveIntegerField(null=True, blank=True)
    water_goal_ml = models.PositiveIntegerField(default=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_bmr(self):
        """Расчет базового метаболизма (BMR)"""
        if self.gender == 'M':
            return 88.362 + (13.397 * float(self.weight)) + (4.799 * self.height) - (5.677 * self.age)
        else:
            return 447.593 + (9.247 * float(self.weight)) + (3.098 * self.height) - (4.330 * self.age)
    
    def calculate_tdee(self):
        """Расчет суточной нормы калорий (TDEE)"""
        bmr = self.calculate_bmr()
        return bmr * float(self.activity_level)
    
    def calculate_calorie_goal(self):
        """Расчет целевой нормы с учетом цели"""
        tdee = self.calculate_tdee()
        if self.goal == 'lose':
            return tdee - 500
        elif self.goal == 'gain':
            return tdee + 500
        return tdee
    
    def save(self, *args, **kwargs):
        if not self.daily_calorie_goal:
            self.daily_calorie_goal = int(self.calculate_calorie_goal())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Профиль {self.user.username}"