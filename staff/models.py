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
        
class Staff(BaseModel):
    first_name = models.CharField(max_length=250, null=False, blank=False)
    last_name = models.CharField(max_length=250, null=False, blank=False)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    phone = models.CharField(max_length=250, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    employee_id = models.CharField(max_length=250, null=False, blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"