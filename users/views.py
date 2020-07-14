# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import bcrypt
from django.db.models import Model
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view


def index(request):
    return HttpResponse("Inside User")


@api_view(['POST'])
def login(request):
    print(request)
    phone_num = request.data["phone_num"]
    password = request.data["password"].encode("utf-8")
    try:
        user = User.objects.all().get(phone_num=phone_num)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if bcrypt.checkpw(password, user.password.encode("utf-8")):
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search(request):
    print(request)
    if "phone_num" in request.GET:
        phone_num = request.GET["phone_num"]
        try:
            user = User.objects.all().get(phone_num=phone_num)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):

    def get(self, request, pk=None):
        if not pk:
            users = User.objects.all()
            print(users)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            user = User.objects.all().get(id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)

    def put(self, request, pk=None):
        print("inside API Put")
        errors = {"errors": []}
        if not pk:
            errors["errors"].append("Must Include id while making PUT request")
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        new_password = request.data.get('password')
        try:
            user = User.objects.all().get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        print(user)
        user.password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt((15)))
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, pk=None):
        if pk:
            error = {"errors": "Must Not Include id while making PUT request"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        print("Inside Post")
        try:
            user = User.objects.all().get(id=request.data["id"])
        except ObjectDoesNotExist:
            user_dict = request.data.dict()
            print(type(user_dict))
            user_dict["password"] = bcrypt.hashpw(user_dict["password"].encode("utf-8"), bcrypt.gensalt((15)))
            print(user_dict)
            new_user = User(**user_dict)
            new_user.save()
            print(new_user.password)
            serializer = UserSerializer(new_user)
            return Response(serializer.data)
        error = {"errors": "User Id already exists "}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)