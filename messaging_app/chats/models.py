from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('GUEST', 'guest'),
        ('HOST', 'host'),
        ('ADMIN', 'admin')
    ]
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=False, db_index=True)
    role = models.CharField(choices=ROLE_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Using email as login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.username}'


class Property(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                   editable=False, db_index=True)
    host_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='property')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price_per_night = models.DecimalField(decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'pending'),
        ('CONFIRMED', 'confirmed'),
        ('CANCELLED', 'cancelled')
    ]
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False, db_default=True)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE,
                                    related_name='bookings')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    total_price = models.DecimalField(decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False, db_index=True)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE,
                                   related_name='payments')
    amount = models.DecimalField(decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 editable=False, db_index=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='review')
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE,
                                    related_name='review')
    rating = models.IntegerField(choices=[(i, i)for i in range(1, 6)])
    comment = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                       editable=False, db_index=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'conversation: {self.conversation_id}'


# Model for Messages
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False, db_index=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='sent_message')
    recipient_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='recieved_message')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,
                                     related_name='messages')

    message_body = models.TextField(max_length=220, null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender_id.username} @ {self.sent_at}: {
            self.message_body[:30]}'

