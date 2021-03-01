from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .forms import LoginForm, SignUpForm
from .services import DashboardService
from django import template

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })


def index(request):
    
    context = {}
    context['segment'] = 'index'
    context['detected_today'] = DashboardService.get_detected_today()
    context['detected_this_week'] = DashboardService.get_detected_this_week()
    context['detected_this_month'] = DashboardService.get_detected_this_month()
    context['detected_per_day'] = DashboardService.get_detected_per_day()
    context['detected_last_30_days_grouped'] = DashboardService.get_detected_last_30_days_grouped()

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template = request.path.split('/')[-1]
        return load_page(request, context, load_template)

    except Exception as e:
    
        print(e)
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

def load_page(request, context, template_name):
    try:
        context['segment'] = template_name
        
        html_template = loader.get_template( template_name )
        return HttpResponse(html_template.render(context, request))
        
    except (template.TemplateDoesNotExist, IsADirectoryError):

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print(e)
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))