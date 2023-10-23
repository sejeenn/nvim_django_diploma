import json

from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse

from rest_framework.views import APIView


class LoginView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        user = authenticate(
            request,
            username=body['username'],
            password=body['password']
        )
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return HttpResponse(status=200)


