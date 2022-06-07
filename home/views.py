import folium as f
from django.shortcuts import render

m = f.Map(location=[27.70630934201652, 85.33001138998168], zoom_start=18, no_touch=True,
               disable_3d=True, zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
f.Marker(
    location=[27.70630934201652, 85.33001138998168],
    popup="Softwarica College",
    icon=f.Icon(color="red", icon="info-sign"),
).add_to(m)

f.Marker(
    location=[27.707236688115596, 85.33096855258636],
    popup="Spot 1",
    icon=f.Icon(color="blue", icon="info-sign"),
).add_to(m)

f.Marker(
    location=[27.704956969288983, 85.32898367537017],
    popup="Spot 1",
    icon=f.Icon(color="green", icon="info-sign"),
).add_to(m)
f.TileLayer('openstreetmap').add_to(m)


def homepage(request):
    if request.method == 'GET':
        print(request.user)
        return render(request, 'home.html', {'user': request.user})

    elif request.method == 'POST':
        return render(request, 'home.html')


def explore(request):
    if request.method == 'GET':
        return render(request, 'explore.html', {'user': request.user})


def packages(request):
    global m
    if request.method == 'GET':
        return render(request, 'package.html', {'user': request.user, 'm': m._repr_html_()})

def profile(request):
    if request.method == 'GET':
        return render(request, 'profile.html', {'user': request.user})
