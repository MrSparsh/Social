# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
        ]

    def __str__(self):
        return self.name

