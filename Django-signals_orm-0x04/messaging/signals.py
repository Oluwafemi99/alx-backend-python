from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory, User


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


# signal to delete all related object after User deletion
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # delete all messages where user is the sender
    Message.objects.filter(sender=instance).delete()
    # delete all message where user is the receiver
    Message.objects.filter(receiver=instance).delete()
    # delete all User notification
    Notification.objects.filter(user=instance).delete()
    # delete all message history
    MessageHistory.objects.filter(edited_by=instance).delete()
