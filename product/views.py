import io
import json
import random
import datetime
from datetime import timezone
#django
from django.urls import reverse
from django.db.models import Q,Sum,Min,Max 
from django.db import transaction, IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
# rest framework
from rest_framework import status
#local
from main.decorators import role_required
from main.functions import generate_form_errors, get_auto_id, has_group,log_activity
from product.models import MaterialTypeCategory, Materials, MaterialsType, Product, ProductCategory, ProductImage, ProductSubCategory
from product.forms import MaterialsForm, MaterialsTypeForm, ProductCategoryForm, ProductForm, ProductImageForm, ProductSubCategoryForm

# Create your views here.
def get_sub_category(request):
    category = request.GET.get('category')
    print(category)
    instances = ProductSubCategory.objects.filter(product_category__pk=category,is_deleted=False)
    print(instances)
    data = {
        'instances': list(instances.values('id', 'name')),
        }
    return JsonResponse(data)

def get_materials_type(request):
    material = request.GET.get('material')
    instances = MaterialsType.objects.filter(material__pk=material,is_deleted=False)
    data = {
        'instances': list(instances.values('id', 'name')),
        }
    return JsonResponse(data)

def get_materials_type_category(request):
    material_type = request.GET.get('material_type')
    instances = MaterialTypeCategory.objects.filter(material_type__pk=material_type,is_deleted=False)
    data = {
        'instances': list(instances.values('id', 'name')),
        }
    return JsonResponse(data)

@login_required
# @role_required(['superadmin'])
def material_info(request,pk):
    """
    Material List
    :param request:
    :return: Material List single view
    """
    
    instance = Materials.objects.get(pk=pk)

    context = {
        'instance': instance,
        'page_name' : 'Material Info',
        'page_title' : 'Material Info',
    }

    return render(request, 'admin_panel/pages/product/materials/info.html', context)

@login_required
# @role_required(['superadmin'])
def material_list(request):
    """
    material
    :param request:
    :return: material list view
    """
    filter_data = {}
    query = request.GET.get("q")
    
    instances = Materials.objects.filter(is_deleted=False).order_by("-date_added")
    
    if query:
        instances = instances.filter(
            Q(invoice_no__icontains=query) |
            Q(sales_id__icontains=query) 
        )
        title = "material list - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Materials List',
        'page_title' : 'Materials List',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/pages/product/materials/list.html', context)

@login_required
# @role_required(['superadmin'])
def create_material(request):
    MaterialsTypeFormset = formset_factory(MaterialsTypeForm, extra=2)
    
    if request.method == 'POST':
        material_form = MaterialsForm(request.POST)
        material_type_formset = MaterialsTypeFormset(request.POST, prefix='material_type_formset', form_kwargs={'empty_permitted': False})
        
        form_is_valid = False
        if material_form.is_valid():
            form_is_valid = True
            print(material_form.cleaned_data.get("is_subcategory"))
            if material_form.cleaned_data.get("is_subcategory") == True:
                if not material_type_formset.is_valid():
                    form_is_valid = False
        
        if form_is_valid:
            try:
                with transaction.atomic():
                    material_data = material_form.save(commit=False)
                    material_data.auto_id = get_auto_id(Materials)
                    material_data.creator = request.user
                    material_data.save()
                    
                    if material_data.is_subcategory :
                        for form in material_type_formset:
                            material_type = form.save(commit=False)
                            material_type.auto_id = get_auto_id(MaterialsType)
                            material_type.creator = request.user
                            material_type.material = material_data
                            material_type.save()

                            if material_type.is_subcategory: 
                                sub_categories = form.cleaned_data['sub_category_name'].split(',')
                                for sub_category in sub_categories:
                                    sub_category = sub_category.strip()
                                    MaterialTypeCategory.objects.create(
                                        auto_id=get_auto_id(MaterialTypeCategory),
                                        creator=request.user,
                                        name=sub_category,
                                        material_type=material_type,
                                    )
                                log_activity(
                                    created_by=request.user,
                                    description=f"created material-- '{material_data}'"
                                    )
                    
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "Materials created successfully.",
                        'redirect': 'true',
                        "redirect_url": reverse('product:material_list')
                    }
            except IntegrityError as e:
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }

            except Exception as e:
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }
        else:
            message = generate_form_errors(material_form, formset=False)
            if material_form.cleaned_data.get("is_subcategory"):
                message += generate_form_errors(material_type_formset, formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
                "form_errors": material_form.errors.as_json(),
                "formset_errors": material_type_formset.errors,
            }

        return JsonResponse(response_data)
    
    else:
        material_form = MaterialsForm()
        material_type_formset = MaterialsTypeFormset(prefix='material_type_formset')
        
        context = {
            'material_form': material_form,
            'material_type_formset': material_type_formset,
            'page_name': 'Create Material',
            'page_title': 'Create Materials',
            'url': reverse('product:create_material'),
            'material_page': True,
            'is_need_select2': True,
        }
        
        return render(request, 'admin_panel/pages/product/materials/create.html', context)
    
    
@login_required
# @role_required(['superadmin'])
def edit_material(request,pk):
    """
    Edit operation of material
    :param request:
    :param pk:
    :return:
    """
    material_instance = get_object_or_404(Materials, pk=pk)
    metirial_types = MaterialsType.objects.filter(material=material_instance)

    if MaterialsType.objects.filter(material=material_instance).exists():
        i_extra = 0
    else:
        i_extra = 1

    MaterialTypesFormset = inlineformset_factory(
        Materials,
        MaterialsType,
        extra=i_extra,
        form=MaterialsTypeForm,
    )

    message = ''

    if request.method == 'POST':
        material_form = MaterialsForm(request.POST,files=request.FILES,instance=material_instance)
        material_type_formset = MaterialTypesFormset(request.POST,instance=material_instance,prefix='material_type_formset',form_kwargs={'empty_permitted': False})

        if material_form.is_valid() and material_type_formset.is_valid():
            try:
                with transaction.atomic():
                    # Update purchase data
                    material_form_instance = material_form.save(commit=False)
                    material_form_instance.date_updated = datetime.datetime.today().now()
                    material_form_instance.updater = request.user
                    material_form_instance.save()
                    
                    if material_instance.is_subcategory or material_form_instance.is_subcategory :
                        for form in material_type_formset:
                            if form not in material_type_formset.deleted_forms:
                                item_data = form.save(commit=False)
                                if not item_data.auto_id:
                                    item_data.material = material_form_instance
                                    item_data.auto_id = get_auto_id(MaterialsType)
                                    item_data.creator = request.user
                                    item_data.updater = request.user
                                    item_data.date_updated = datetime.datetime.today().now()
                                item_data.save()
                                
                                MaterialTypeCategory.objects.filter(material_type=item_data).delete()
                                
                                if item_data.is_subcategory:
                                    sub_categories = form.cleaned_data['sub_category_name'].split(',')

                                    for sub_category in sub_categories:
                                        sub_category = sub_category.strip()

                                        MaterialTypeCategory.objects.create(
                                            auto_id=get_auto_id(MaterialTypeCategory),
                                            creator=item_data.creator,
                                            updater=request.user,
                                            date_added=item_data.date_added,
                                            date_updated=datetime.datetime.today().now(),
                                            name=sub_category,
                                            material_type=item_data,
                                        )

                        for form in material_type_formset.deleted_forms:
                            form.instance.delete()
                        log_activity(
                            created_by=request.user,
                            description=f"edited material--'{material_instance}'"
                            )

                    response_data = {
                        "status": "true",
                        "title": "Successfully Updated",
                        "message": "Materials updated successfully.",
                        "redirect": "true",
                        "redirect_url": reverse('product:material_list'),
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
            message = generate_form_errors(material_form, formset=False)
            message += generate_form_errors(material_type_formset, formset=True)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        material_form = MaterialsForm(instance=material_instance)
        material_type_formset = MaterialTypesFormset(queryset=metirial_types,
                                               prefix='material_type_formset',
                                               instance=material_instance)
        context = {
            'material_form': material_form,
            'material_type_formset': material_type_formset,

            'message': message,
            'page_name': 'edit material',
            'is_purchase_pages': True,
            'is_purchase_page': True,
        }

        return render(request, 'admin_panel/pages/product/materials/create.html', context)
    

@login_required
# @role_required(['superadmin'])
def delete_material(request,pk):
    """
    material deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    material = Materials.objects.get(pk=pk)
    material.is_deleted = True
    material.save()
    
    material_type = MaterialsType.objects.filter(material=material)
    material_type.update(is_deleted = True)
    
    type_ids = material_type.values_list("pk")
    MaterialTypeCategory.objects.filter(material_type__pk__in=type_ids).update(is_deleted = True)
    log_activity(
                created_by=request.user,
                description=f"Deleted material '{material}'"
            )
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Material Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:material_list'),
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
# @role_required(['superadmin'])
def product_category_list(request):
    """
    product category
    :param request:
    :return: product category list view
    """
    filter_data = {}
    query = request.GET.get("q")
    
    instances = ProductCategory.objects.filter(is_deleted=False).order_by("-date_added")
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query)
        )
        title = "product category list - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Product Category List',
        'page_title' : 'Product Category List',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/pages/product/category/list.html', context)


@login_required
# @role_required(['superadmin'])
def create_product_category(request):
    ProductSubCategoryFormset = formset_factory(ProductSubCategoryForm, extra=2)
    
    message = ''
    if request.method == 'POST':
        product_category_form = ProductCategoryForm(request.POST,files=request.FILES)
        sub_product_formset = ProductSubCategoryFormset(request.POST,prefix='sub_product_formset', form_kwargs={'empty_permitted': False})
        
        form_is_valid = False
        if product_category_form.is_valid():
            form_is_valid = True
            if product_category_form.cleaned_data.get("is_subcategory"):
                if not sub_product_formset.is_valid():
                    form_is_valid = False
        
        if  form_is_valid :
            try:
                with transaction.atomic():
                    product_data = product_category_form.save(commit=False)
                    product_data.auto_id = get_auto_id(ProductCategory)
                    product_data.creator = request.user
                    product_data.save()
                    
                    if product_data.is_subcategory:
                        for form in sub_product_formset:
                            sub_category = form.save(commit=False)
                            sub_category.auto_id = get_auto_id(ProductSubCategory)
                            sub_category.creator = request.user
                            sub_category.product_category = product_data
                            sub_category.save()

                        log_activity(
                            created_by=request.user,
                            description=f"Created product category '{product_data}'"
                            )
                        
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "Materials created successfully.",
                        'redirect': 'true',
                        "redirect_url": reverse('product:product_category_list')
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
            message = generate_form_errors(product_category_form, formset=False)
            if product_category_form.cleaned_data.get("is_subcategory"):
                message += generate_form_errors(sub_product_formset, formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        product_category_form = ProductCategoryForm(request.POST)
        sub_product_formset = ProductSubCategoryFormset(prefix='sub_product_formset')
        
        context = {
            'product_category_form': product_category_form,
            'sub_product_formset': sub_product_formset,
            
            'page_name' : 'Create Product Category',
            'page_title': 'Create Product Category',
            'url': reverse('product:create_product_category'),
            
            'product_page': True,
            'is_need_select2': True,
            
        }
        
        return render(request,'admin_panel/pages/product/category/create.html',context)
    
    
@login_required
# @role_required(['superadmin'])
def edit_product_category(request,pk):
    """
    Edit operation of product_category
    :param request:
    :param pk:
    :return:
    """
    product_category_instance = get_object_or_404(ProductCategory, pk=pk)
    product_sub_categories = ProductSubCategory.objects.filter(product_category=product_category_instance)

    if ProductSubCategory.objects.filter(product_category=product_category_instance).exists():
        i_extra = 0
    else:
        i_extra = 1

    MaterialTypesFormset = inlineformset_factory(
        ProductCategory,
        ProductSubCategory,
        extra=i_extra,
        form=ProductSubCategoryForm,
    )

    message = ''

    if request.method == 'POST':
        product_category_form = ProductCategoryForm(request.POST,files=request.FILES,instance=product_category_instance)
        sub_product_formset = MaterialTypesFormset(request.POST,instance=product_category_instance,prefix='sub_product_formset',form_kwargs={'empty_permitted': False})

        if product_category_form.is_valid() and sub_product_formset.is_valid():
            try:
                with transaction.atomic():
                    # Update purchase data
                    product_category_form_instance = product_category_form.save(commit=False)
                    product_category_form_instance.date_updated = datetime.datetime.today().now()
                    product_category_form_instance.updater = request.user
                    product_category_form_instance.save()

                    for form in sub_product_formset:
                        if form not in sub_product_formset.deleted_forms:
                            item_data = form.save(commit=False)
                            if not item_data.auto_id:
                                item_data.product_category = product_category_form_instance
                                item_data.auto_id = get_auto_id(ProductSubCategory)
                                item_data.updater = request.user
                                item_data.date_updated = datetime.datetime.today().now()
                            item_data.save()
                            
                    for form in sub_product_formset.deleted_forms:
                        form.instance.delete()
                    log_activity(
                        created_by=request.user,
                        description=f"edited product category '{product_category_instance}'"
                        )

                    response_data = {
                        "status": "true",
                        "title": "Successfully Updated",
                        "message": "Product Category updated successfully.",
                        "redirect": "true",
                        "redirect_url": reverse('product:product_category_list'),
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
            message = generate_form_errors(product_category_form, formset=False)
            message += generate_form_errors(sub_product_formset, formset=True)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        product_category_form = ProductCategoryForm(instance=product_category_instance)
        sub_product_formset = MaterialTypesFormset(queryset=product_sub_categories,
                                               prefix='sub_product_formset',
                                               instance=product_category_instance)
        context = {
            'product_category_form': product_category_form,
            'sub_product_formset': sub_product_formset,

            'message': message,
            'page_name': 'edit product_category',
            'is_purchase_pages': True,
            'is_purchase_page': True,
        }

        return render(request, 'admin_panel/pages/product/category/create.html', context)
    

@login_required
# @role_required(['superadmin'])
def delete_product_category(request,pk):
    """
    product_category deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    product_category = ProductCategory.objects.get(pk=pk)
    product_category.is_deleted = True
    product_category.save()
    
    product_category_type = ProductSubCategory.objects.filter(product_category=product_category)
    product_category_type.update(is_deleted = True)
    log_activity(
                created_by=request.user,
                description=f"Deleted product category-- '{product_category}'"
            )
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:product_category_list'),
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
# @role_required(['superadmin'])
def product_info(request,pk):
    """
    Product Info
    :param request:
    :return: Product Info single view
    """
    
    instance = Product.objects.get(pk=pk)
    images_instances = ProductImage.objects.filter(product=instance)

    context = {
        'instance': instance,
        'images_instances': images_instances,
        
        'page_name' : 'Product Info',
        'page_title' : 'Product Info',
    }

    return render(request, 'admin_panel/pages/product/product/info.html', context)

@login_required
# @role_required(['superadmin'])
def product_list(request):
    """
    product
    :param request:
    :return: product list view
    """
    filter_data = {}
    query = request.GET.get("q")
    
    instances = Product.objects.filter(is_deleted=False).order_by("-date_added")
    
    if query:
        instances = instances.filter(
            Q(name__icontains=query)
        )
        title = "product list - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Product List',
        'page_title' : 'Product List',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/pages/product/product/list.html', context)


@login_required
# @role_required(['superadmin'])
def create_product(request):
    ProductImageFormset = formset_factory(ProductImageForm, extra=2)
    
    message = ''
    if request.method == 'POST':
        product_form = ProductForm(request.POST,files=request.FILES)
        product_image_formset = ProductImageFormset(request.POST,files=request.FILES,prefix='product_image_formset', form_kwargs={'empty_permitted': False})
        
        if product_form.is_valid() and product_image_formset.is_valid() :
            try:
                with transaction.atomic():
                    product_data = product_form.save(commit=False)
                    product_data.auto_id = get_auto_id(Product)
                    product_data.creator = request.user
                    product_data.save()
                    
                    for form in product_image_formset:
                        product_image = form.save(commit=False)
                        product_image.auto_id = get_auto_id(ProductImage)
                        product_image.creator = request.user
                        product_image.product = product_data
                        product_image.save()
                    log_activity(
                        created_by=request.user,
                        description=f"Created product-- '{product_data}'"
                        )
                        
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "Product created successfully.",
                        'redirect': 'true',
                        "redirect_url": reverse('product:product_list')
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
            message = generate_form_errors(product_form, formset=False)
            message += generate_form_errors(product_image_formset, formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        product_form = ProductForm()
        product_image_formset = ProductImageFormset(prefix='product_image_formset')
        
        context = {
            'product_form': product_form,
            'product_image_formset': product_image_formset,
            
            'page_name' : 'Create Product',
            'page_title': 'Create Product',
            'url': reverse('product:create_product'),
            
            'product_page': True,
            'is_need_select2': True,
            
        }
        
        return render(request,'admin_panel/pages/product/product/create.html',context)
    
    
@login_required
# @role_required(['superadmin'])
def edit_product(request,pk):
    """
    Edit operation of product
    :param request:
    :param pk:
    :return:
    """
    product_instance = get_object_or_404(Product, pk=pk)
    product_images = ProductImage.objects.filter(product=product_instance)

    if ProductImage.objects.filter(product=product_instance).exists():
        i_extra = 0
    else:
        i_extra = 1

    ProductImagesFormset = inlineformset_factory(
        Product,
        ProductImage,
        extra=i_extra,
        form=ProductImageForm,
    )

    message = ''

    if request.method == 'POST':
        product_form = ProductForm(request.POST,files=request.FILES,instance=product_instance)
        product_image_formset = ProductImagesFormset(request.POST,files=request.FILES,instance=product_instance,prefix='product_image_formset',form_kwargs={'empty_permitted': False})

        if product_form.is_valid() and product_image_formset.is_valid():
            try:
                with transaction.atomic():
                    # Update purchase data
                    product_form_instance = product_form.save(commit=False)
                    product_form_instance.date_updated = datetime.datetime.today().now()
                    product_form_instance.updater = request.user
                    product_form_instance.save()

                    for form in product_image_formset:
                        if form not in product_image_formset.deleted_forms:
                            item_data = form.save(commit=False)
                            if not item_data.auto_id:
                                item_data.product = product_form_instance
                                item_data.auto_id = get_auto_id(ProductImage)
                                item_data.updater = request.user
                                item_data.date_updated = datetime.datetime.today().now()
                            item_data.save()
                            
                    for form in product_image_formset.deleted_forms:
                        form.instance.delete()
                    log_activity(
                        created_by=request.user,
                        description=f"Updated product '{product_instance}'"
                        )

                    response_data = {
                        "status": "true",
                        "title": "Successfully Updated",
                        "message": "Product updated successfully.",
                        "redirect": "true",
                        "redirect_url": reverse('product:product_list'),
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
            message = generate_form_errors(product_form, formset=False)
            message += generate_form_errors(product_image_formset, formset=True)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        product_form = ProductForm(instance=product_instance)
        product_image_formset = ProductImagesFormset(queryset=product_images,
                                               prefix='product_image_formset',
                                               instance=product_instance)
        context = {
            'product_form': product_form,
            'product_image_formset': product_image_formset,

            'message': message,
            'page_name': 'edit product',
            'is_purchase_pages': True,
            'is_purchase_page': True,
        }

        return render(request, 'admin_panel/pages/product/product/create.html', context)
    

@login_required
# @role_required(['superadmin'])
def delete_product(request,pk):
    """
    product deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    product = Product.objects.get(pk=pk)
    product.is_deleted = True
    product.save()
    
    product_image = ProductImage.objects.filter(product=product)
    product_image.update(is_deleted = True)

    log_activity(
                created_by=request.user,
                description=f"Deleted product -- '{product_image}'"
            )
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:product_list'),
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
# @role_required(['superadmin'])
def delete_product_image(request,pk):
    """
    product image deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    product_image = ProductImage.objects.get(pk=pk)
    product_image.is_deleted = True
    product_image.save()
    log_activity(
                created_by=request.user,
                description=f"Deleted product image-- '{product_image}'"
            )
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Image Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:product_list'),
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')