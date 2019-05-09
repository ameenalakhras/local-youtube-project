from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User



@require_http_methods(['POST'])
def create_user(request):
    """
    creates a user if the email and the user name doesn't exist
    """
    message = False
    status_color = False

    username = request.POST['username']
    email = request.POST['email']
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    password = request.POST['password']
    password_confirmation = request.POST['password_confirmation']

    user_exists = User.objects.filter(username=username)
    email_exists = User.objects.filter(email=email)

    if user_exists:
        message = "this name is already taken, please choose another one"
        status_color = "danger"

    elif email_exists:
        message = "this email is already taken, please choose another one"
        status_color = "danger"

    else:
        if password == password_confirmation :
            user = User.objects.create(
                email=email,
                username=username,
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

    return HttpResponseRedirect("/")


@require_http_methods(['POST'])
def login_auth(request):
    """
    log-in authentication for the user
    """
    username = request.POST['loginUsername']
    password = request.POST['loginPassword']
    user = authenticate(username=username , password=password)
    try:
        login(request, user)
        HttpResponseRedirect('/')
    except Exception as e:
        print("Error :", e)
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
            print("user is an admin")
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect("/")
    return render(request, "login.html")


def log_out(request):
    """
    logs out the user and removes it's session
    """
    logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    """
    returns signup page html
    """
    return render(request, "signup.html")
