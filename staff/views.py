import io
import json
import random
import datetime
from datetime import timezone, datetime
#django
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q,Sum,Min,Max 
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.http import JsonResponse
# rest framework
from rest_framework import status
#local
from staff.forms import *
from staff.models import *
from main.decorators import role_required
from main.functions import generate_form_errors, get_auto_id, has_group
from work_order.views import log_activity

# Create your views here.

@login_required
def tile_list(request):
    """
    Tile details list view
    :param request:
    :return: Tile details list view
    """
    filter_data = {}
    query = request.GET.get("q")

    instances = Tile.objects.all()

    if query:
        instances = instances.filter(Q(name__icontains=query))
        title = "Tile List - %s" % query
        filter_data['q'] = query

    context = {
        'instances': instances,
        'page_name': 'Tile List',
        'page_title': 'Tile List',
        'filter_data': filter_data,
    }

    return render(request, 'admin_panel/pages/tile/tile_list.html', context)


@login_required
def tile_info(request, pk):
    """
    Tile single view
    :param request:
    :return: Tile details single view
    """
    instance = get_object_or_404(Tile, pk=pk)

    context = {
        'instance': instance,
        'page_name': 'Tile Info',
        'page_title': 'Tile Info',
    }

    return render(request, 'admin_panel/pages/tile/tile_info.html', context)


@login_required
def tile_create(request):
    """
    Create Tile
    :param request:
    :return: JSON response for success or failure
    """
    if request.method == 'POST':
        form = TileForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Tile created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:tile_list')
            }

        else:
            message = form.errors.as_json()
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = TileForm()

        context = {
            'form': form,
            'page_name': 'Create Tile',
            'page_title': 'Create Tile',
            'url': reverse('staff:tile_create'),
        }

        return render(request, 'admin_panel/pages/tile/tile_create.html', context)


@login_required
def tile_edit(request, pk):
    """
    Edit Tile
    :param request:
    :return: JSON response for success or failure
    """
    instance = get_object_or_404(Tile, pk=pk)

    if request.method == 'POST':
        form = TileForm(request.POST, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Tile updated successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:tile_list')
            }

        else:
            message = form.errors.as_json()
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = TileForm(instance=instance)

        context = {
            'form': form,
            'page_name': 'Edit Tile',
            'page_title': 'Edit Tile',
            'url': reverse('staff:tile_edit', kwargs={'pk': pk}),
        }

        return render(request, 'admin_panel/pages/tile/tile_edit.html', context)


@login_required
def tile_delete(request, pk):
    """
    Delete Tile
    :param request:
    :return: JSON response for success or failure
    """
    instance = get_object_or_404(Tile, pk=pk)

    instance.delete()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Tile successfully deleted.",
        "redirect": "true",
        "redirect_url": reverse('staff:tile_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

#department
@login_required
# @role_required(['superadmin'])
def department_info(request, pk):
    """
    Department List
    :param request:
    :return: Department details List single view
    """
    
    instance = get_object_or_404(Department, pk=pk)

    context = {
        'instances': instance,
        'page_name': 'Department',
        'page_title': 'Department',
    }

    return render(request,'admin_panel/pages/department/department_info.html', context)

@login_required
# @role_required(['superadmin'])
def department_list(request):
    """
    Department details
    :param request:
    :return: Department details list view
    """
    filter_data = {}
    query = request.GET.get("q")
    
    instances = Department.objects.filter(is_deleted=False).order_by("-date_added")
    name=request.GET.get('name')
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query)
        )
        title = "Department details list - %s" % query
        filter_data['q'] = query

    elif name:
        instances=instances.filter(name__icontains=name)
    
    context = {
        'instances': instances,
        'page_name': 'Department Details List',
        'page_title': 'Department Details List',
        'filter_data': filter_data,
    }

    return render(request,'admin_panel/pages/department/department_list.html', context)

@login_required
# @role_required(['superadmin'])
def department_create(request):
    """
    Create operation of department details
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Department)
            data.creator = request.user
            data.save()
            log_activity(
                created_by=request.user,
                description=f"created department-- '{data}'"
            )
            
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Department created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:department_list')
            }
    
        else:
            message = generate_form_errors(form, formset=False)
           
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        form = DepartmentForm()
        
        context = {
            'form': form,
            'page_name': 'Create Department',
            'page_title': 'Create Department',
            'url': reverse('staff:department_create'),
        }
        
        return render(request,'admin_panel/pages/department/department_create.html', context)
    
@login_required
# @role_required(['superadmin'])
def department_edit(request, pk):
    """
    Edit operation of department details
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=instance)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            log_activity(
                created_by=request.user,
                description=f"Updated department '{instance}'"
            )
                    
            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Department updated successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:department_list')
            }
    
        else:
            message = generate_form_errors(form, formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        form = DepartmentForm(instance=instance)

        context = {
            'form': form,
            'page_name': 'Edit Department',
            'page_title': 'Edit Department',
            'url': reverse('staff:department_edit', kwargs={'pk': pk}),
        }

        return render(request,'admin_panel/pages/department/department_edit.html', context)
    

@login_required
# @role_required(['superadmin'])
def department_delete(request, pk):
    """
    Department deletion
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Department, pk=pk)
    
    instance.is_deleted = True
    instance.save()
    log_activity(
                created_by=request.user,
                description=f"deleted department-- '{instance}'"
            )
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Department successfully deleted.",
        "redirect": "true",
        "redirect_url": reverse('staff:department_list'),
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
# @role_required(['superadmin'])
def designation_info(request, pk):
    """
    Designation List
    :param request:
    :return: Designation details List single view
    """
    
    instance = get_object_or_404(Designation, pk=pk)

    context = {
        'instances': instance,
        'page_name': 'Designation',
        'page_title': 'Designation',
    }

    return render(request,'admin_panel/pages/designation/designation_info.html', context)

@login_required
# @role_required(['superadmin'])
def designation_list(request):
    """
    Designation details
    :param request:
    :return: Designation details list view
    """
    filter_data = {}
    query = request.GET.get("q")
    
    instances = Designation.objects.filter(is_deleted=False).order_by("-date_added")
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query)
        )
        title = "Designation details list - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name': 'Designation Details List',
        'page_title': 'Designation Details List',
        'url': reverse('staff:designation_list'),
        'filter_data': filter_data,
    }

    return render(request, 'admin_panel/pages/designation/designation_list.html', context)

@login_required
# @role_required(['superadmin'])
def designation_create(request):
    """
    Create operation of designation details
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Designation)
            data.creator = request.user
            data.save()
            form.save_m2m() 
            
            log_activity(
                created_by=request.user,
                description=f"created designation '{data}'"
            )
            
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Designation created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:designation_list')
            }
    
        else:
            message = generate_form_errors(form, formset=False)
           
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        form = DesignationForm()
        
        context = {
            'form': form,
            'page_name': 'Create Designation',
            'page_title': 'Create Designation',
            'url': reverse('staff:designation_create'),
        }
        
        return render(request, 'admin_panel/pages/designation/designation_create.html', context)

@login_required
# @role_required(['superadmin'])
def designation_edit(request, pk):
    """
    Edit operation of designation details
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Designation, pk=pk)
    
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=instance)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.today()
            data.updater = request.user
            data.save()
            form.save_m2m()
            log_activity(
                created_by=request.user,
                description=f"edited designation-- '{instance}'"
            )
                    
            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Designation updated successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:designation_list')
            }
    
        else:
            message = generate_form_errors(form, formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        form = DesignationForm(instance=instance)

        context = {
            'form': form,
            'page_name': 'Edit Designation',
            'page_title': 'Edit Designation',
            'url': reverse('staff:designation_edit', kwargs={'pk': pk}),
        }

        return render(request,'admin_panel/pages/designation/designation_edit.html', context)

@login_required
# @role_required(['superadmin'])
def designation_delete(request, pk):
    """
    Designation deletion
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Designation, pk=pk)
    
    instance.is_deleted = True
    instance.save()
    log_activity(
                created_by=request.user,
                description=f"Deleted designation----'{instance}'"
            )
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Designation successfully deleted.",
        "redirect": "true",
        "redirect_url": reverse('staff:designation_list'),
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

#----------------------------Staff --------------------------
@login_required
# @role_required(['superadmin'])
def staff_info(request,pk):
    """
    Staff Information
    :param request:
    :return: staff information single view
    """
    
    instances = Staff.objects.get(pk=pk)

    context = {
        'instances': instances,
        'page_name' : 'Staff',
        'page_title' : 'Staff',
    }

    return render(request, 'admin_panel/pages/staff/staff_info.html', context)

@login_required
# @role_required(['superadmin'])
def staff_list(request):
    """
    Staff List
    :param request:
    :return: Staff List  view
    """
    filter_data = {}
    query = request.GET.get("q")
    
    instances = Staff.objects.filter(is_deleted=False).order_by("-date_added")
    
    if query:
        instances = instances.filter(
            Q(department__name__icontains=query) |
            Q(designation__name__icontains=query) 
        )
        title = "Staff list - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Staff List',
        'page_title' : 'Staff List',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/pages/staff/staff_list.html', context)

@login_required
# @role_required(['superadmin'])
def staff_create(request):
    """
    create operation of staff create
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = StaffForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    user_data = User.objects.create_user(
                        username=f'{form.cleaned_data.get("first_name")}123',
                        password=f'{form.cleaned_data.get("first_name")}@123',
                        is_active=True,
                        )
                                
                    group_names = ["staff",form.cleaned_data["designation"].name,form.cleaned_data["department"].name]

                    for group_name in group_names:
                        if Group.objects.filter(name=group_name).exists():
                            group = Group.objects.get(name=group_name)
                        else:
                            group = Group.objects.create(name=group_name)
                        user_data.groups.add(group)
            
                    data = form.save(commit=False)
                    data.auto_id = get_auto_id(Staff)
                    data.creator = request.user
                    data.user = user_data
                    data.save()
                    log_activity(
                        created_by=request.user,
                        description=f"Created staff '{user_data}'"
                        )
                    
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "Staff created successfully.",
                        'redirect': 'true',
                        "redirect_url": reverse('staff:staff_list')
                    }
                    
            except IntegrityError as e:
                # Handle database integrity error
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }

            except Exception as e:
                # Handle other exceptions
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }
    
        else:
            message = generate_form_errors(form, formset=False)
           
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        form = StaffForm(request.POST)
        
        context = {
            'form': form,
            'page_name' : 'Create Staff',
            'page_title': 'Create Staffs',
            'url': reverse('staff:staff_create'),
            
            'staff_page': True,
            'is_need_select2': True,
            
        }
        
        return render(request,'admin_panel/pages/staff/staff_create.html',context)


@login_required
# @role_required(['superadmin'])
def staff_edit(request,pk):
    """
    edit operation of staff
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Staff, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = StaffForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            log_activity(
                created_by=request.user,
                description=f"Updated staff-- '{instance}'"
            )
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Staff Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:staff_list')
            }
    
        else:
            message = generate_form_errors(form ,formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        
        form = StaffForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Staff',
            'page_title' : 'Edit Staff',
            'url' : reverse('staff:staff_edit', kwargs={'pk': pk}),
            
            'is_need_datetime_picker': True,
            'is_need_forms': True,
        }

        return render(request, 'admin_panel/pages/staff/staff_create.html',context)    


@login_required
# @role_required(['superadmin'])
def staff_delete(request, pk):
    """
    Staff deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = Staff.objects.get(pk=pk)
    
    instance.is_deleted = True
    instance.save()
    log_activity(
                created_by=request.user,
                description=f"Deleted staff '{instance}'"
            )
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Staff Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('staff:staff_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
# @role_required(['superadmin'])
def attendence_list(request):
    
    if request.method == "GET":
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d')
        instances = Attendance.objects.filter(is_deleted=False, date = formatted_date)

        context = {
            'instances': instances,
            'page_name' : 'Attendence List',
            'page_title' : 'Attendence List'
        }
        return render(request, 'admin_panel/pages/attendence/attendence_list.html', context)
    



def get_staffs(request):
    if request.method == "GET":
        search_name = request.GET.get('input_name')
        relate_names = Staff.objects.filter(first_name__icontains=search_name)
        names = list(relate_names.values())
        dat = {'names': names}
        return JsonResponse(dat)


def add_staff_to_list(request):
    if request.method == "GET":
        search_name = request.GET.get('input_name')
        relate_names = Staff.objects.filter(auto_id=search_name)
        names_list = list(relate_names.values())
        dat = {'names_list': names_list}
        return JsonResponse(dat)


def adding_attendence(request):
    if request.method == "GET":
        search_name = request.GET.get('checked_items')
        print(search_name,"########################")
        auto_id_list = search_name.split(",") if "," in search_name else list(search_name)
        print("auto_id_list", auto_id_list)
        relate_names = Staff.objects.filter(auto_id=search_name)
        names_list = list(relate_names.values())
        dat = {'names_list': names_list}
        # return JsonResponse(dat)
        message = "bijoy"
        response_data = {
        "status": "false",
        "title": "Failed",
        "message": message}
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')



@login_required
# @role_required(['superadmin'])
def attendence_create(request):
    if request.method == "GET":
        context = {
            'page_name' : 'Create Staff',
            'page_title': 'Create Staffs',
            'url': reverse('staff:attendence_create'),
            'staff_page': True,
            'is_need_select': True,
        }
        return render(request,'admin_panel/pages/attendence/attendence_create.html',context)
    
    if request.method == "POST":
        checked_list = request.POST.getlist('staff_checkbox')
        print("checked_list", checked_list)
        
        success_count = 0
        unsuccess_count = 0
        for check in checked_list:
            staff_instance = Staff.objects.get(auto_id = check)
            max_attendence = Attendance.objects.aggregate(Max('auto_id'))['auto_id__max']
            max_attendence = 0 if max_attendence == None else max_attendence
            current_date = datetime.now()
            formatted_date = current_date.strftime('%Y-%m-%d')
            existsts = Attendance.objects.filter(staff__auto_id = staff_instance.auto_id , date = formatted_date).exists()
            print("aaaaaaaaaaa", existsts)
            if existsts:
                unsuccess_count += 1
            else:
                attendance=Attendance.objects.create(
                    creator = request.user,
                    auto_id = int(max_attendence) + 1,
                    attendance = '010',
                    punchin_time =  datetime.now().time(),
                    date = datetime.now().date(),
                    staff = staff_instance
                )
                success_count += 1
        
        if len(checked_list) == (success_count + unsuccess_count):
            log_activity(
                created_by=request.user,
                description=f"created attendance-- '{attendance}'"
            )
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Attendence Added successfully.",
                'redirect': 'true',
                "redirect_url": reverse('staff:attendence_list')
            }
        
        else:
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": "Something went Wrong, Please try again later !",
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

 
@login_required
# @role_required(['superadmin'])
def attendence_edit(request, pk):
    
    instance = get_object_or_404(Attendance, pk=pk)
    message = ''
    
    if request.method == "GET":
        form = AttendenceForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Attendence',
            'page_title' : 'Edit Attendence',
            'url' : reverse('staff:attendence_edit', kwargs={'pk': pk}),
            'is_need_datetime_picker': True,
            'is_need_forms': True,
        }
        return render(request, 'admin_panel/pages/attendence/attendence_edit.html',context)
    
    if request.method == 'POST':
        form = AttendenceForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.today()
            data.updater = request.user
            data.save()

            log_activity(
                created_by=request.user,
                description=f"Updated attendance --'{instance}'"
            )
                    
            response_data = {
                "status": "true", 
                "title": "Successfully Created", 
                "message": "Attendence Update successfully.", 
                'redirect': 'true',
                "redirect_url": reverse('staff:attendence_list')
            }
        else:
            message = generate_form_errors(form ,formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    

@login_required
# @role_required(['superadmin'])
def attendance_delete(request, pk):
    
    instance = Attendance.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    log_activity(
                created_by=request.user,
                description=f"Deleted attendance '{instance}'"
            )
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Attendance Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('staff:attendence_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

