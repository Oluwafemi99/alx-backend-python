from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status, filters, permissions
from .models import Conversation, Message
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOrSender, IsParticipantOfConversation
from .pagination import MessagePagination
from . filters import Messagefilter
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participant__email']
    permission_classes = [IsParticipantOrSender, IsParticipantOfConversation,
                          permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Get messages for a specific conversation
        """
        conversation = self.get_object()
        if request.user not in conversation.participants.all():
            return Response({'detail: you are noy Authorised'},
                            status=status.HTTP_403_FORBIDDEN)
        messages = Message.objects.filter(conversation_id=conversation.id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['message_body', 'sender_id__email']
    permission_classes = [IsParticipantOrSender, permissions.IsAuthenticated]
    pagination_class = MessagePagination
    filterset_class = Messagefilter

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender_id=user) | Message.objects.filter(
            recipient_id=user)

    def perform_create(self, serializer):
        return serializer.save(sender_id=self.request.user)
