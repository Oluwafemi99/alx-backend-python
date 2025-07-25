from rest_framework import permissions


class IsParticipantOrSender(permissions.BasePermission):
    """ Permissions to allow only conversation participant
and message sender and reciecer to only access the object
"""
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Permission for message object
        if hasattr(obj, 'sender_id'):
            return obj.sender_id == user or obj.recipient_id == user

        # permission for conversation object
        if hasattr(obj, "participant"):
            return user in obj.participant.all()

        return False


class IsParticipantOfConversation(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_autheticated

    def has_object_permission(self, request, view, obj):

        if hasattr(obj, 'participant'):
            return request.user in obj.participant.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.all()
        return False
