from django.shortcuts import render

# Create your views here.
def admindashboard(request):
    return render(request, 'admin_layout.html')