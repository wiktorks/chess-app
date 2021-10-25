from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, EmailField, CharField, ValidationError, Serializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from users.models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'matches_won', 'matches_lost',
                  'matches_draw', 'description']


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile_serializer = ProfileSerializer(
            instance=instance.profile, data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()

        return super().update(instance, validated_data)


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


class PasswordResetSerializer(Serializer):
    old_password = CharField(min_length=8, write_only=True,
                             required=True)
    new_password = CharField(min_length=8, write_only=True,
                             required=True, validators=[validate_password])
    new_password2 = CharField(min_length=8, write_only=True,
                              required=True, validators=[validate_password])

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise ValidationError('Password fields did not match')

        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise ValidationError('Wrong user password provided')

        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
