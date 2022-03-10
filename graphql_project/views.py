from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from graphql_project.models import User

class test(GenericViewSet):
    def list_user(self, request):
        user = User.objects.filter(id = 3).values("name")
        return Response(data=user, status=200)