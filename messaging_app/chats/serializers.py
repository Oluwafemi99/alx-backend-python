from rest_framework import serializers
from models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        feilds = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.object.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    sender_id = UserSerializer
    recipient_id = UserSerializer

    class Meta:
        models = Message
        feilds = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer
    message = MessageSerializer

    class Meta:
        model = Conversation
        feilds = '__all__'
