from datetime import datetime
from rest_framework import status
from rest_framework.response import Response


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        with open('request.log', 'a') as log_file:
            log_file.write(log_entry)
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access only between 18 (6PM) and 21 (9PM)
        if not (18 <= current_hour < 21):
            return Response({'Error:'}, status=status.HTTP_403_FORBIDDEN)
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        