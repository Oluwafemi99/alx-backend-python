from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


# Create your views here.
@require_POST
@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return HttpResponse('Your accont has been succefully deleted')
