from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Message


# Create your views here.
@require_POST
@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return HttpResponse('Your accont has been succefully deleted')


# view for threaded message replies
def threaded_messages(request):
    # Fetch root messages and prefetch replies
    messages = Message.objects.filter(
        parent_message__isnull=True, sender=request.user).select_related(
            'sender', 'receiver').prefetch_related('replies')
    return render(request, 'threaded_messages.html', {'messages': messages})
