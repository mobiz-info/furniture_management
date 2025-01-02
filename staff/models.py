from django.db import models
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField

from main.models import BaseModel

ATTENDANCE_CHOICES = (
    ('010', 'Present'),
    ('015', 'Absent'),
    ('020', 'Sick Leave'),
    ('025', 'Casual Leave'),
    ('030', 'Paid Leave'),
    ('035', 'Other'),
)

LEAVE_DURATION_CHOICES = (
    ('010', 'Half Day'),
    ('015', 'Full Day'),
)

LEAVE_STATUS_CHOICES = (
    ('101', 'Requested'),
    ('105', 'Approved'),
    ('108', 'Rejected'),
    ('110', 'Cancelled'),
)

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
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    employee_id = models.CharField(max_length=250)
    date_of_birth = models.DateField(null=True, blank=True)
    image = VersatileImageField('Image', upload_to="staff/profile", blank=True, null=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"
        
    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_initial(self):
        first_name = self.first_name[0] if self.first_name else ''
        last_name = self.last_name[0] if self.last_name else ''
        return first_name + last_name

class Attendance(BaseModel):
    date = models.DateField()
    attendance = models.CharField(max_length=3, choices=ATTENDANCE_CHOICES)
    punchin_time = models.TimeField(blank=True, null=True)
    punchout_time = models.TimeField(blank=True, null= True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="attendance_staff")
    class Meta:
        db_table = 'attendance'
        verbose_name = ('Attendance')
        verbose_name_plural = ('Attendance')
        unique_together = ('staff', 'date')

    def __str__(self):
        return f'{self.staff.user.username} - {self.attendance}'
