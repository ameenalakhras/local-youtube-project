from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from .models import Custome_User as User


@require_http_methods(['POST'])
def login_auth(request):
    """
    log-in authentication for the user
    """
    email = request.POST['loginEmail']
    password = request.POST['loginPassword']
    user = authenticate(email=email , password=password)
    try:
        login(request, user)
        HttpResponseRedirect('/')
    except:
        print("Error")
    return HttpResponseRedirect('/login')


def user_login(request):
    """
    uses login authentication [login_auth()]
    authenticated >> redirected to admin page
    if not authenticated >> redirected to the login page
    """
    print("login works")
    if request.user.is_active:
        print("this is an active user")
    if request.user.is_authenticated:
        print("user authenticated")
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect("/")
    return render(request, "login.html")

def log_out(request):
    """
    logs out the user and removes it's session
    """
    logout(request)
    return HttpResponseRedirect('/')


def temp(request):
    """
    this is a function to test all of the new views/templates and it's located at '/temp'
    """
    return render(request,"signup.html",None)


def signup(request):
    """
    returns signup page html
    """
    return render(request, "signup.html")


@require_http_methods(['POST'])
def create_user(request):
    """
    creates a user if the email and the user name doesn't exist
    """
    message = False
    status_color = False

    username = request.POST['username']
    email = request.POST['email']
    birth_day = request.POST['dateOfBirth']
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    password = request.POST['password']
    password_confirmation = request.POST['password_confirmation']

    user_exists = User.objects.filter(username=username)
    email_exists = User.objects.filter(email=email)

    if user_exists:
        message = "this name is used before"
        status_color = "danger"

    elif email_exists:
        message = "this email is used already"
        status_color = "danger"

    else:
        if password == password_confirmation :
            user = User.objects.create(
                email=email,
                username=username,
                birth_day = birth_day,
                first_name = first_name,
                last_name = last_name,
                is_staff=True,
                is_superuser=False,
                is_active=True,

            )
            user.set_password(password)
            user.save()

            # user_group = Group.objects.get(name='normal user')
            # user_group.user_set.add(user)
            # user_group.save()

            if user:
                message = "the account has been added sucessfully"
                status_color = "success"
        else:
            message = "the two passwords doesn't match"
            status_color = "danger"

    context = {
        'message' : message,
        'status_color' : status_color
    }
    print(message)

    return HttpResponseRedirect("/")
