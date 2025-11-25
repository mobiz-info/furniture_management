import json
# django
from django import template
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http.response import HttpResponseRedirect, HttpResponse
# local
from main.functions import get_current_role

register = template.Library()

def role_required(roles):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            current_role = get_current_role(request)
            if not current_role in roles:
                if request.is_ajax():
                    response_data = {
                        "status": "false",
                        "stable": "true",
                        "title": "Permission Denied",
                        "message": "You have no permission to do this action."
                    }
                    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                else:
                    context = {
                        "title": "Permission Denied"
                    }
                    return render(request, 'errors/403.html', context)

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper

def is_user_authenticated(request):
    return request.user.is_authenticated