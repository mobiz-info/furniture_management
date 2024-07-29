from django.db import models
from main.models import BaseModel
from django.contrib.auth.models import User
# Create your models here.
class Department(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "department"
        verbose_name = "Department"
        verbose_name_plural = "Departments"

class Designation(BaseModel):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "designation"
        verbose_name = "Designation"
        verbose_name_plural = "Designations"