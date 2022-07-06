import folium as f
from django.shortcuts import render, redirect

from dashboard.forms import CreateOrderForm
from dashboard.models import Package, Order

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
    order: CreateOrderForm
    if not package:
        return redirect('explore')
    if request.method == 'GET':
        order = CreateOrderForm()
        context['form'] = order
    if request.method == 'POST':
        order = CreateOrderForm(request.POST.copy())
        order.data['customer'] = request.user
        order.data['package'] = package
        order.data['status'] = Order.STATUS[0][0]
        hasOrdered = bool(Order.objects.filter(customer_id=request.user.id).filter(package_id=package.id).filter(
            status__exact='pending'))
        if order.is_valid() and not hasOrdered and package.status == 'available':
            print("ORDER PLACED")
            order.save()
        else:
            print("ORDER REJECT")
            print(order.errors)
        context['form'] = order
    context['package'] = package


    return render(request, 'package.html', context)
