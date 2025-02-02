from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from datetime import date

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    height = serializers.FloatField(validators=[MinValueValidator(0.1)])
    weight = serializers.FloatField(validators=[MinValueValidator(0.1)])
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 'height', 'weight', 'date_of_birth', 'fitness_level')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        return value

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        
        if 'date_of_birth' in data:
            if data['date_of_birth'] > date.today():
                raise serializers.ValidationError("Date of birth cannot be in the future")
            
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    height = serializers.FloatField(validators=[MinValueValidator(0.1)])
    weight = serializers.FloatField(validators=[MinValueValidator(0.1)])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'height', 'weight', 'date_of_birth', 'fitness_level')
        read_only_fields = ('id', 'username', 'email')

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future")
        return value
