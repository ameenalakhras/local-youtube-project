from django.shortcuts import render

# Create your views here.



def mainPage(request):
    """
    the main page of the website
    """

    return render(request, template_name="mainPage.html" ,context=None )


def temp(request):
    """
    a temporary function for adding new features
    """

    return render(request, template_name="temp.html", context=None)
