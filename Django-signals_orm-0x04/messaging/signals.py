from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


# signal to create notification when a new message is triggered
@receiver(post_save, sender=Message)
def create_notification_on_message(instance, created, sender, **kwargs):
    if created:
        Notification.objects.create(user=instance.reciever, message=instance)


# Signal to log old content before a message is updated
@receiver(pre_save, sender=Message)
def log_history(instance, sender, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != old_message.instance:
                MessageHistory.objects.create(message=instance,
                                              old_content=old_message.content)
                instance.edited = True
        except Message.DoesNotExist:
            pass
