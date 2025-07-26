from rest_framework import serializers
from .models import Conversation, Message
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
    sender = serializers.StringRelatedField(read_only=True)
    recipient = serializers.StringRelatedField(read_only=True)
    message_preview = serializers.SerializerMethodField()

    class Meta:
        models = Message
        feilds = '__all__'

    def validate_message_body(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Messagebody must be at least 5 characters long.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer
    message = MessageSerializer

    class Meta:
        model = Conversation
        feilds = '__all__'
