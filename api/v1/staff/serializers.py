from rest_framework import serializers

from customer . models import Customer
from staff.models import Attendance, Staff


class Staff_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id','auto_id', 'first_name', 'last_name']

class Staff_Attendecne_List_Serializer(serializers.ModelSerializer):
    staff = Staff_Serializer()
    class Meta:
        model = Attendance
        fields = ['id', 'auto_id', 'date', 'attendance', 'punchin_time', 'punchout_time', 'staff']