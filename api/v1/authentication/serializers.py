from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from six import text_type

from staff.models import Attendance, Staff

class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(UserTokenObtainPairSerializer, cls).get_token(user)
        return token
    
    def validate(cls, attrs):
        data = super(UserTokenObtainPairSerializer, cls).validate(attrs)

        refresh = cls.get_token(cls.user)

        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)

        if cls.user.is_superuser:
            data['role'] = "superuser"
        else:
            data['role'] = "user"

        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.save()
        return user


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class ResetPasswordSerializer(serializers.Serializer):
    member_id = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def member_id_validate(self, data):
        if data["member_id"] == "":
          raise serializers.ValidationError("member_id missed")

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']

        if password == "":
            raise serializers.ValidationError("Enter a valid password")
        
        if confirm_password == "":
            raise serializers.ValidationError("Re-enter Password")

        if len(password) < 8:
            raise serializers.ValidationError("Password should be at least 8 characters")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        return data
    
    
class StaffSerializer(serializers.ModelSerializer):
    initial = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    designation_name = serializers.SerializerMethodField()
    attendance_status = serializers.SerializerMethodField()
    attendance_key = serializers.SerializerMethodField()
    attendance_value = serializers.SerializerMethodField()
    punchin_time = serializers.SerializerMethodField()
    punchout_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Staff
        fields = ['id','employee_id','first_name','last_name','email','phone','date_of_birth','department','designation','profile_image','initial','department_name','designation_name','attendance_status','attendance_key','attendance_value','punchin_time','punchout_time']
        
    def get_initial(self,obj):
        return obj.get_initial().upper()
    
    def get_profile_image(self,obj) :
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        
    def get_department_name(self,obj):
        return obj.department.name
    
    def get_designation_name(self,obj):
        return obj.designation.name
    
    def get_attendance_status(self,obj):
        return Attendance.objects.filter(staff=obj,date=datetime.today().date()).exists()
    
    def get_attendance_key(self,obj):
        key = ""
        if (instances:=Attendance.objects.filter(staff=obj,date=datetime.today().date())).exists():
            key = instances.first().attendance
        return key
    
    def get_attendance_value(self,obj):
        value = ""
        if (instances:=Attendance.objects.filter(staff=obj,date=datetime.today().date())).exists():
            value = instances.first().get_attendance_display()
        return value
    
    def get_punchin_time(self,obj):
        time = ""
        if (instances:=Attendance.objects.filter(staff=obj,date=datetime.today().date())).exists():
            time = instances.first().punchin_time.strftime("%I:%M %p")
        return time
    
    def get_punchout_time(self,obj):
        time = ""
        if (instances:=Attendance.objects.filter(staff=obj,date=datetime.today().date())).exists() and instances.first().punchout_time != None :
            time = instances.first().punchout_time.strftime("%I:%M %p")
        return time
    
class UserSerializer(serializers.Serializer):
    group_names = serializers.SerializerMethodField()
    initial = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['firstname','lastname','group_names']
    
    def get_group_names(self, obj):
        group_names = obj.user.groups.all()
        return [group.name for group in group_names]
    
    def get_initial(self,obj):
        firstname = self.firstname[0] if self.firstname else ''
        lastname = self.lastname[0] if self.lastname else ''
        return firstname.upper() + lastname.upper()