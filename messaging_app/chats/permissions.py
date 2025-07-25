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
