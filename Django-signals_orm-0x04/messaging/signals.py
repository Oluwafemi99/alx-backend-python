from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


# signal to create notification when a new message is triggered
@receiver(post_save, sender=Message)
def create_notification_on_message(instance, created, sender, **kwargs):
    if created:
        Notification.objects.create(user=instance.reciever, message=instance)
