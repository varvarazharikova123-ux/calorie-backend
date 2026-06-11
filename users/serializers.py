from rest_framework import serializers
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    activity_level = serializers.DecimalField(max_digits=4, decimal_places=3, coerce_to_string=False)
    
    class Meta:
        model = Profile
        fields = ['gender', 'age', 'height', 'weight', 'activity_level', 'goal', 'daily_calorie_goal', 'water_goal_ml']

    def validate_activity_level(self, value):
        try:
            return Decimal(str(value))
        except:
            return Decimal('1.375')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'created_at']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile']
    
    def create(self, validated_data):
        from decimal import Decimal
        profile_data = validated_data.pop('profile')
        
        # Конвертируем activity_level в Decimal
        if 'activity_level' in profile_data:
            profile_data['activity_level'] = Decimal(str(profile_data['activity_level']))
        
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user