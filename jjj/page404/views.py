from django.shortcuts import render
from django.shortcuts import render_to_response

# Create your views here.


def handler404(request, exception, template_name="404.html"):
    """
    retuns custome 404 page (when debug mode isn't activated)
    """
    response = render_to_response("404.html")
    response.status_code = 404
    return response

# on the main website urls you should type :
# from django.conf.urls import handler404
#
# handler404 = 'page404.views.handler404'
