from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb.settings import EMAIL_FROM_DEFAULT

from .models import User


class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
        )
        if created:
            password = str(user.pk) + str(user.username) + str(user.email)
            user.set_password(password)
        user.is_active = False
        user.save()
        confirmation_code = default_token_generator.make_token(user)
        valid = default_token_generator.check_token(user, confirmation_code)
        send_mail(
            f'Confirmaton code for {username}',
            f'Code: \n{confirmation_code} \nis_valid: \n{valid}',
            EMAIL_FROM_DEFAULT,
            (email,)
        )
        return user

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                "Can't create user 'me' by some very important reason."
            )
        if User.objects.filter(
                username=data['username'],
                email=data['email']).exists():
            return data
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                "A user with that username already exists."
            )
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                "A user with that email already exists."
            )
        return data


class UserTokenSerializer(serializers.Serializer):
    username = serializers.SlugField(
        required=True,
        max_length=150
    )
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
                user, data['confirmation_code']):
            raise serializers.ValidationError(
                'Confirmation code is invalid or expired.'
            )
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role'
        )
