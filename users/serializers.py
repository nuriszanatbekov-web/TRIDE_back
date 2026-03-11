from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterStep1Serializer(serializers.Serializer):
    """1-кадам: Негизги маалыматтар"""
    email         = serializers.EmailField()
    first_name    = serializers.CharField(max_length=100)
    last_name     = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    gender        = serializers.ChoiceField(choices=[('M', 'Эркек'), ('F', 'Аял')])

    def validate_email(self, value):
        # Эгер бул email менен активдүү колдонуучу бар болсо — ката
        if User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError('Бул email катталган!')
        return value


class VerifyEmailSerializer(serializers.Serializer):
    """Email кодун текшерүү"""
    email = serializers.EmailField()
    code  = serializers.CharField(max_length=6)


class ResendCodeSerializer(serializers.Serializer):
    """Кодду кайра жөнөтүү үчүн email"""
    email = serializers.EmailField()


class RegisterStep2Serializer(serializers.Serializer):
    """2-кадам: Физикалык маалыматтар + сырсөз"""
    email            = serializers.EmailField()
    weight           = serializers.FloatField(min_value=20, max_value=300)
    height           = serializers.FloatField(min_value=50, max_value=250)
    password         = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Сырсөздөр дал келбейт!'})
        return data


class LoginSerializer(serializers.Serializer):
    """Кириш"""
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """Профиль"""
    class Meta:
        model  = User
        fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'weight', 'height']
        read_only_fields = ['id', 'email']