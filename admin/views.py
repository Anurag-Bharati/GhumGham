from django.shortcuts import render

# Create your views here.
def admindashboard(request):
    return render(request, 'admins_home.html')
