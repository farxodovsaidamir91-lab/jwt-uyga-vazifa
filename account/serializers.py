from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import CustomUser


class SignUpSerialzier(serializers.ModelSerializer):
    conf_pass = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'username', 'password', 'conf_pass']

    def validate(self, data):
        password = data.get('password')
        conf_pass = data.get('conf_pass')

        if password != conf_pass and password and conf_pass:
            raise ValidationError('Parollar mos emas')
        return data

    def create(self, validated_data):
        validated_data.pop('conf_pass', None)
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'msg': 'user created',
            'user': data
        }



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError('Login yoki parol xato')
        
        attrs['user'] = user
        return attrs



class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username']
        read_only_fields = ['username']



class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    conf_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        conf_password = attrs.get('conf_password')

        user = self.context['request'].user

        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'Eski parol xato kiritildi.'})

        if new_password != conf_password:
            raise ValidationError({'conf_password': 'Yangi parollar birbiriga mos emas.'})

        if old_password == new_password:
            raise ValidationError({'new_password': 'Yangi parol eski paroldan farq qilishi kerak.'})

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user