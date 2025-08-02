from django.db import models
import uuid
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager

User = get_user_model()


# Create your models here.
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='message')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='message')
    content = models.TextField(max_length=255, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE,
                                       related_name='replies', null=True,
                                       blank=True)
    read = models.BooleanField(default=False)
    unread = UnreadMessagesManager()

    def __str__(self):
        return f'From {self.sender} To {self.receiver}'

# method to retrieves all message replies
    def get_all_replies(self):
        # recursive fetch for all replies
        replies = []

        def fetch_replies(message):
            children = message.replies.all()
            for child in children:
                replies.append(child)
                fetch_replies(child)
        fetch_replies(self)
        return replies


class MessageHistory(models.Model):
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False, db_index=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE,
                                related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='history')

    def __str__(self):
        return f'History:{self.message.message_id} at {self.edited_at}'


class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                       editable=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='notification')
    message = models.ForeignKey(Message, on_delete=models.CASCADE,
                                related_name='notification')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user}, Message: {self.message.
                                                         message_id}'
