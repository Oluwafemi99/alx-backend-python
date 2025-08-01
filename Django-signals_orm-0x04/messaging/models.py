from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model


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

    def __str__(self):
        return f'From {self.sender} To {self.receiver}'


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


# signal to create notification when a new message is triggered
@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
