import folium as f
from django.contrib import messages
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.views.generic import ListView

from dashboard.config import At
from dashboard.forms import CreateOrderForm
from dashboard.models import Package, Order
from home.forms import UpdateProfileForm
from users.auth import has_session
from users.models import User
from datetime import date


def getMap(coordinate: [float], data: [[str, str, list[float]]] = [], zoom: int = 18) -> f.Map:
    # assert data is not None and data.__len__() > 0
    m = f.Map(location=coordinate, zoom_start=zoom, no_touch=True, disable_3d=True,
              zoom_control=True, scrollWheelZoom=False, dragging=True)
    f.Marker(
        location=coordinate,
        popup="test",
        icon=f.Icon(color='red', icon="info-sign"),
    ).add_to(m)
    for item in data:
        f.Marker(
            location=item[2],
            popup=item[0],
            icon=f.Icon(color=item[1], icon="info-sign"),
        ).add_to(m)
    f.TileLayer('cartodbpositron').add_to(m)
    return m


def homepage(request):
    p = Package.objects.filter(is_featured=True)
    context: dict = {'user': request.user, 'packages': p}
    return render(request, 'home.html', context, status=200)


class Explore(ListView):
    model = Package
    template_name = 'explore.html'
    context_object_name = 'packages'
    paginate_by = 4
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(Explore, self).get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', None)
        return context

    def get_queryset(self):
        filter_val = self.request.GET.get('search', None)

        if filter_val == 'featured':
            new_context = Package.objects.filter(is_featured=True)
        elif filter_val == 'new':
            new_context = Package.objects.all().order_by('-id')
        elif filter_val == 'short':
            new_context = Package.objects.filter(duration__lte=3)
        elif filter_val == 'long':
            new_context = Package.objects.filter(duration__gt=3)
        elif filter_val == 'eco':
            new_context = Package.objects.filter(price__lte=100)
        elif filter_val and not filter_val == '#':
            new_context = Package.objects.filter(name__icontains=filter_val)
        else:
            new_context = Package.objects.all().order_by('id')
        return new_context


def packages(request, identity):
    context = {'user': request.user}
    package = Package.objects.get(id=identity)
    order: CreateOrderForm
    if not package:
        return redirect('explore')
    coordinate = package.itinerary.places.all()[0].coordinate.split(',')
    latlng: [float] = [float(coordinate[0]), float(coordinate[1])]
    m = getMap(latlng)
    if request.method == 'GET':
        order = CreateOrderForm()
        order.fields['date'].widget.attrs['min'] = date.today()
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
    context['m'] = m._repr_html_()
    return render(request, 'package.html', context)


def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to view your profile")
        return redirect("auth")
    user = User.objects.get(id=request.user.id)
    form = UpdateProfileForm(instance=user)
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    order_count = Order.objects.filter(customer_id=user.id).filter(status__exact='approved').count()
    account_age = date.today() - user.created_date
    account_age = account_age.__str__().split(',')[0]
    account_age = account_age.split(' ')
    context = {'user': request.user, 'form': form, 'order_count': order_count, 'account_age': account_age}
    return render(request, 'profile.html', context)



def statement(request):
    if request.method == 'GET':
        return HttpResponse("STATEMENT PAGE")


def update_profile(request):
    if request.method == 'GET':
        return redirect('profile')
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        if user:
            email = request.POST.get('email', None)
            address = request.POST.get('address', None)
            if not user.email == email:
                user.email = email
            if not user.address == address:
                user.address = address
            user.save()
        return redirect('profile')


def myBookings(request):
    order = Order.objects.filter(customer_id=request.user.id)
    count = order.count()
    return HttpResponse(f'{count}')


def cancelBooking(request, oid):
    order = Order.objects.get(id=oid)
    if not order.status == 'pending':
        return redirect('get-my-orders')
    order.status = Order.STATUS[3][0]
    order.save()
    return redirect('get-my-orders')
