from django.shortcuts import render


# Create your views here.


def homepage(request):
    if request.method == 'GET':
        print(request.user)
        return render(request, 'home.html', {'user': request.user})

    elif request.method == 'POST':
        return render(request, 'home.html')


def explore(request):
    if request.method == 'GET':
        return render(request, 'explore.html', {'user': request.user})
