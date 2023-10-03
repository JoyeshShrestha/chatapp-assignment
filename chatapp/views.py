from django.http import HttpResponse
def home_page(request):
    print("home page requested")
    return HttpResponse("This is home page")  