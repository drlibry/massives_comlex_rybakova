from uuid import uuid4

from django.db import models

class NumberArray(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    numbers = models.TextField()  # Хранит массив чисел в виде JSON строки


class ComplexNumber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    real = models.FloatField()
    imaginary = models.FloatField()

