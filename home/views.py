from django.shortcuts import render


# Create your views here.


def homepage(request):
    if request.method == 'GET':
        print(request.user)
        return render(request, 'index.html', {'user': request.user.username})

    elif request.method == 'POST':
        return render(request, 'index.html')
