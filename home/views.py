import folium as f
from django.shortcuts import render, redirect

from dashboard.models import Package

m = f.Map(location=[27.70630934201652, 85.33001138998168], zoom_start=18, no_touch=True,
          disable_3d=True, zoom_control=True,
          scrollWheelZoom=False,
          dragging=True)
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
f.TileLayer('cartodbpositron').add_to(m)


def homepage(request):
    p = Package.objects.filter(is_featured=True)

    if request.method == 'GET':
        print(request.user)
        return render(request, 'home.html', {'user': request.user, 'packages': p})

    elif request.method == 'POST':
        return render(request, 'home.html')


def explore(request):
    if request.method == 'GET':
        p = Package.objects.exclude(status__exact="unavailable")
        return render(request, 'explore.html', {'user': request.user, 'packages': p})


def packages(request, identity):
    global m
    context = {'user': request.user, 'm': m._repr_html_()}
    package = Package.objects.get(id=identity)
    if not package:
        return redirect('explore')
    if request.method == 'GET':
        context['package'] = package
        print(package.itinerary.places.all())
        return render(request, 'package.html', context)
