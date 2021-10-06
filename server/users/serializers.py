from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, EmailField, CharField, ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from users.models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

# Update zrobić w Views
    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        # instance.profile = validated_data['profile']

        return instance


class RegisterUserSerializer(ModelSerializer):
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = CharField(min_length=8, write_only=True,
                         required=True, validators=[validate_password])
    password2 = CharField(min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError('Password fields did not match')
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
