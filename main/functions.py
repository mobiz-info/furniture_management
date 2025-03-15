#Standard
import string
import random
import random
import string
from cryptography.fernet import Fernet
#Django
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.core.mail import EmailMessage, EmailMultiAlternatives
#Third Party
from random import randint
from datetime import timezone
from main.models import Processing_Log


def generate_unique_id(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_form_errors(args,formset=False):
    i = 1
    message = ""
    if not formset:
        for field in args:	
            if field.errors:
                message += "\n"
                message += field.label + " : "
                message += str(field.errors)

        for err in args.non_field_errors():
            message += str(err)
    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message += "\n"
                    message += field.label + " : "
                    message += str(field.errors)
            for err in form.non_field_errors():
                message += str(err)

    message = message.replace("<li>", "")
    message = message.replace("</li>", "")
    message = message.replace('<ul class="errorlist">', "")
    message = message.replace("</ul>", "")
    return message

def generate_member_form_errors(args,formset=False):
    i = 1
    message = ""
    if not formset:
        for field in args:
            if field.errors:
                message += "\n"
                message += field.name + " : "
                message += str(field.errors)

        for err in args.non_field_errors():
            message += str(err)
    elif formset:
        for form in args:
           
            for field in form:
                if field.errors:
                    message += "\n"
                    message += field.name + " : "
                    message += str(field.errors)
            for err in form.non_field_errors():
                message += str(err)

    message = message.replace("<li>", "")
    message = message.replace("</li>", "")
    message = message.replace('<ul class="errorlist">', "")
    message = message.replace("</ul>", "")
    return message
    

def get_auto_id(model):
    auto_id = 1
    try:
        latest_auto_id =  model.objects.all().order_by("-date_added")[:1]
        if latest_auto_id:
            for auto in latest_auto_id:
                auto_id = auto.auto_id + 1
    except:
        pass
    return auto_id


def get_current_role(request):
    is_superadmin = False
    is_staff = False
    is_dealer = False
    is_core_team = False
    is_office_executive = False
    is_field_executive = False

    if request.user.is_authenticated:        
        
        if User.objects.filter(id=request.user.id,is_superuser=True,is_active=True).exists():
            is_superadmin = True
        
        if User.objects.filter(id=request.user.id,is_active=True,groups__name="staff").exists():
            is_staff = True
            
        if User.objects.filter(id=request.user.id,is_active=True,groups__name="core_team").exists():
            is_core_team = True
            
        if User.objects.filter(id=request.user.id,is_active=True,groups__name="office_executive").exists():
            is_office_executive = True
            
        if User.objects.filter(id=request.user.id,is_active=True,groups__name="field_executive").exists():
            is_field_executive = True

    current_role = "user"
    if is_superadmin:
        current_role = "superadmin"
    elif is_staff:
        current_role = "staff"
    elif is_core_team:
        current_role = "core_team"
    elif is_office_executive:
        current_role = "office_executive"
    elif is_field_executive:
        current_role = "field_executive"
                
    return current_role


def randomnumber(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def paginate(instances, request):
    paginator = Paginator(instances, 20)
    page_number = request.GET.get('page')
    instances = paginator.get_page(page_number)

    return instances


def get_otp(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def load_key():
    key = getattr(settings, "PASSWORD_ENCRYPTION_KEY", None)
    if key:
        return key
    else:
        raise ImproperlyConfigured("No configuration  found in your PASSWORD_ENCRYPTION_KEY setting.")


def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return(encrypted_message.decode("utf-8"))


def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())
    return decrypted_message.decode()

    
    

def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Group.DoesNotExist:
        return False
    

def log_activity(created_by,description,created_date=None,):

    Processing_Log.objects.create(
        created_by=created_by,
        description=description,
    )