import threading
from datetime import date, datetime
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator

from GhumGham import settings

from django.shortcuts import redirect, render
from django.urls import reverse

from GhumGham.settings import GENERATE_DUMMY_DATA

from dashboard.config import At as At
from dashboard.models import ActivityLog, Food, Adventure, Itinerary, Order
from django.views.generic import ListView

from users.models import User
from .forms import CreateUserForm, CreatePlaceForm, CreatePackageForm, CreateAdventureForm, CreateFoodForm, \
    CreateItineraryForm, CreateOrderForm
from .models import Package, Place
from django.utils import timezone


def delete_log(request, identity):
    log = ActivityLog.objects.get(pk=identity)
    if not log:
        messages.error(request, 'Sorry! Something went wrong')
        redirect(reverse('dashboard'), '#zero')
    if not request.user.is_superuser:
        messages.success(request, 'Only Superusers can delete log')
        return redirect('dashboard')
    log.delete()
    messages.success(request, 'Log removed successfully')
    return redirect('dashboard')


def ban_unban_user(request, identity, redirect_to):
    logged_user = request.user

    if logged_user.username == "AnonymousUser":
        messages.error(request, 'User Unauthorized')
        if redirect_to == 0:
            return redirect('dashboard')
        elif redirect_to == 1:
            return redirect('customer-table')
        return redirect('customer-table')

    user = User.objects.get(pk=identity)

    if not user:
        messages.error(request, 'Sorry! Something went wrong')
        if redirect_to == 0:
            return redirect('dashboard')
        elif redirect_to == 1:
            return redirect('customer-table')
        return redirect('customer-table')
    if user.is_superuser:
        messages.error(request, 'Sorry! You can\'t ban a superuser')
        if redirect_to == 0:
            return redirect('dashboard')
        elif redirect_to == 1:
            return redirect('customer-table')
        return redirect('customer-table')

    log = ActivityLog(user=logged_user)
    log.target = user.username
    if not user.is_ban:
        log.action = log.ACTION[5][1]
    else:
        log.action = log.ACTION[6][1]
    log.save()
    user.is_ban = not user.is_ban
    user.save()
    messages.success(request, 'User banned successfully')
    if redirect_to == 0:
        return redirect('dashboard')
    elif redirect_to == 1:
        return redirect('customer-table')
    return redirect('customer-table')


def toggle_user_status(request, identity, redirect_to):
    logged_user = request.user
    if logged_user.username == "AnonymousUser":
        messages.error(request, 'User Unauthorized')
        if redirect_to == 0:
            return redirect('dashboard')
        return redirect('customer-table')
    user = User.objects.get(pk=identity)
    if not user:
        messages.error(request, 'Sorry! Something went wrong')
        if redirect_to == 0:
            return redirect('dashboard')
        return redirect('customer-table')
    if user.is_superuser:
        messages.error(request, 'Sorry! You can\'t change status of a superuser')
        if redirect_to == 0:
            return redirect('dashboard')
        return redirect('customer-table')
    log = ActivityLog(user=logged_user)
    log.target = user.username
    if user.is_active:
        log.action = "Deactivated"
    else:
        log.action = "Activated"
    user.is_active = not user.is_active
    user.save()
    log.save()
    if redirect_to == 0:
        return redirect('dashboard')
    return redirect('customer-table')


class Dashboard(ListView):
    model = ActivityLog
    template_name = 'dashboard.html'
    context_object_name = 'logs'
    paginate_by = 4
    ordering = '-id'
    page_kwarg = "page_log"

    p_admin = Paginator(
        User.objects.filter(is_admin__exact=True).values(
            'id', 'username', 'is_ban', 'created_date').order_by("-id"), 3)
    p_customer = Paginator(
        User.objects.filter(is_customer__exact=True).values(
            'id', 'username', 'is_ban', 'created_date').order_by("-id"), 3)
    p_package = Paginator(Package.objects.values(
        'id', 'name', 'is_featured', 'image', 'desc').order_by('-id'), 3)

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['segment'] = 'index'
        context['ap'] = At.at()
        context['user_count'] = User.objects.count()
        context['customer_count'] = User.objects.filter(is_customer__exact=True).count()
        context['admin_count'] = User.objects.count() - context['customer_count']
        context['package_count'] = Package.objects.filter(status__exact="available").count()
        context['package_count_max'] = Package.objects.all().count()
        context['place_count'] = Place.objects.count()
        context['staff_count'] = User.objects.filter(is_staff__exact=True).count()
        context['active_order'] = Order.objects.filter(status__exact='pending').count()
        a_page = self.request.GET.get('a_page', 1)
        c_page = self.request.GET.get('c_page', 1)
        p_page = self.request.GET.get('p_page', 1)

        context['p_admins'] = self.p_admin.page(a_page)
        context['p_customers'] = self.p_customer.page(c_page)
        context['p_packages'] = self.p_package.page(p_page)
        context['packages'] = Package.objects.filter(status__exact="available")

        return context


def delete_package(request, identity):
    if request.method == "GET":
        return redirect('package-table')

    package = Package.objects.filter(id=identity)[0]
    if package:
        messages.success(request, f'Successfully deleted {package.name} package!')
        print(f"Delete {package.name}")
        package.delete()
    else:
        messages.error(request, 'Sorry! Something went wrong.')
    return redirect('package-table')


def delete_adventure(request, identity):
    if request.method == "GET":
        return redirect('adventure-table')

    adventure = Adventure.objects.filter(id=identity)[0]
    if adventure:
        messages.success(request, f'Successfully deleted {adventure.name} package!')
        print(f"Delete {adventure.name}")
        adventure.delete()
    else:
        messages.error(request, 'Sorry! Something went wrong.')
    return redirect('adventure-table')


def delete_food(request, identity):
    if request.method == "GET":
        return redirect('food-table')

    food = Food.objects.filter(id=identity)[0]
    if food:
        messages.success(request, f'Successfully deleted {food.name} food spot!')
        print(f"Delete {food.name}")
        food.delete()
    else:
        messages.error(request, 'Sorry! Something went wrong.')
    return redirect('adventure-table')


def delete_itinerary(request, identity):
    if request.method == "GET":
        return redirect('itinerary-table')

    itinerary = Itinerary.objects.filter(id=identity)[0]
    if itinerary:
        messages.success(request, f'Successfully deleted {itinerary.name} itinerary!')
        print(f"Delete {itinerary.name}")
        itinerary.delete()
    else:
        messages.error(request, 'Sorry! Something went wrong.')
    return redirect('itinerary-table')


def delete_place(request, identity):
    if request.method == "GET":
        return redirect('place-table')

    place = Place.objects.filter(id=identity)[0]
    if place:
        messages.success(request, f'Successfully deleted {place.name} place!')
        print(f"Delete {place.name}")
        place.delete()
    else:
        messages.error(request, 'Sorry! Something went wrong.')
    return redirect('place-table')


def delete_account(request, identity, redirect_to):
    if request.method == "GET":
        if redirect_to == 0:
            return redirect('dashboard')
        return redirect('customer-table')

    user = User.objects.filter(id=identity)[0]
    if user and not user.is_superuser:
        messages.success(request, f'Successfully deleted account named {user.username}!')
        print(f"Delete {user.username}")
        user.delete()
    else:
        messages.error(request, 'Sorry! Something went wrong.')
    if redirect_to == 0:
        return redirect('dashboard')
    return redirect('customer-table')


def featured_package(request, identity):
    package = Package.objects.filter(id=identity)[0]
    if package:
        package.is_featured = not package.is_featured
        package.save()
    return redirect('package-table')


def hide_unhide_package(request, identity):
    package = Package.objects.filter(id=identity)[0]
    if not package:
        return redirect('package-table')
    if package.status == Package.STATUS[0][0]:
        package.status = Package.STATUS[1][0]
    elif package.status == Package.STATUS[1][0]:
        package.status = Package.STATUS[0][0]
    package.save()
    return redirect('package-table')


def approve_order(request, identity):
    order = Order.objects.filter(id=identity)[0]
    if not order:
        return redirect('order-table')
    if order.status == Order.STATUS[0][0]:
        if request.user and not order.staff:
            order.staff = request.user
        order.status = Order.STATUS[1][0]
        order.package.status = Package.STATUS[2][0]
        order.package.save()
        order.save()
    return redirect('order-table')


def decline_order(request, identity):
    order = Order.objects.filter(id=identity)[0]
    if not order:
        return redirect('order-table')
    if order.status == Order.STATUS[0][0]:
        if request.user and not order.staff:
            order.staff = request.user
        order.status = Order.STATUS[2][0]
        order.save()
    return redirect('order-table')


class GetPackages(ListView):
    model = Package
    template_name = 'tables/package_table.html'
    context_object_name = 'packages'
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(GetPackages, self).get_context_data(**kwargs)
        context['segment'] = 'tables'
        context['ap'] = At.at()
        context['active_order'] = Order.objects.filter(status__exact='pending').count()
        return context


class GetAllPackages(ListView):
    model = Package
    template_name = 'packages.html'
    context_object_name = 'packages'
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(GetAllPackages, self).get_context_data(**kwargs)
        context['segment'] = 'tables'
        context['ap'] = At.at()
        context['active_order'] = Order.objects.filter(status__exact='pending').count()
        return context


class GetCustomers(ListView):
    model = User
    template_name = 'tables/customer_table.html'
    context_object_name = 'customers'
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(GetCustomers, self).get_context_data(**kwargs)
        context['segment'] = 'tables'
        context['ap'] = At.at()
        context['customers'] = User.objects.filter(is_customer__exact=True)
        context['active_order'] = Order.objects.filter(status__exact='pending').count()
        return context


class GetStaffs(ListView):
    model = User
    template_name = 'tables/staff_table.html'
    context_object_name = 'staffs'
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(GetStaffs, self).get_context_data(**kwargs)
        context['segment'] = 'tables'
        context['ap'] = At.at()
        context['staffs'] = User.objects.exclude(is_customer__exact=True).exclude(is_superuser__exact=True)
        context['active_order'] = Order.objects.filter(status__exact='pending').count()
        return context


class GetAdventures(ListView):
    model = Adventure
    template_name = 'tables/adventure_table.html'
    context_object_name = 'adventures'
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(GetAdventures, self).get_context_data(**kwargs)
        context['segment'] = 'tables'
        context['ap'] = At.at()
        context['active_order'] = Order.objects.filter(status__exact='pending').count()
        return context


class GetFoods(ListView):
    model = Food
    template_name = 'tables/food_table.html'
    context_object_name = 'foods'
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(GetFoods, self).get_context_data(**kwargs)
        context['segment'] = 'tables'
        context['ap'] = At.at()
        context['active_order'] = Order.objects.filter(status__exact='pending').count()
        return context

def change_pass(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'change-password.html', context)
    if request.method == 'POST':
        u = User.objects.get(id=request.user.id)
        if not u.check_password(request.POST.get('o_pass', None)):
            return redirect('change-pass')
        new_pass = request.POST.get('n_pass', None)
        if new_pass:
            u.set_password(new_pass)
            u.save()
        else:
            messages.error(request, 'Invalid password')
        return redirect('change-pass')


def notify_via_email(msg, user):
    mail = EmailMultiAlternatives(
        f"Hey {user.username}",
        msg,
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    Thread(mail).start()


class Thread(threading.Thread):

    def __init__(self, task):  # pragma: no cover
        self.task = task
        try:
            threading.Thread.__init__(self)
        except Exception as ex:
            print("[Exception in thread] " + ex.__str__())

    def run(self):  # pragma: no cover
        try:
            self.task.send(fail_silently=False)
        except Exception as ex:
            print("[Exception in thread] " + ex.__str__())


def adminProfile(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'profile.html', context)
    if request.method == 'POST':
        redirect('admin-profile')

class GetItineraries(ListView):
    model = Itinerary
    template_name = 'tables/itinerary_table.html'
    context_object_name = 'itineraries'
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(GetItineraries, self).get_context_data(**kwargs)
        context['segment'] = 'tables'
        context['ap'] = At.at()
        context['active_order'] = Order.objects.filter(status__exact='pending').count()
        return context


class GetPlaces(ListView):
    model = Place
    template_name = 'tables/place_table.html'
    context_object_name = 'places'
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(GetPlaces, self).get_context_data(**kwargs)
        context['segment'] = 'tables'
        context['ap'] = At.at()
        context['active_order'] = Order.objects.filter(status__exact='pending').count()
        return context


class GetOrders(ListView):
    model = Order
    template_name = 'tables/order_table.html'
    context_object_name = 'orders'
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(GetOrders, self).get_context_data(**kwargs)
        context['segment'] = 'tables'
        context['ap'] = At.at()
        context['active_order'] = Order.objects.filter(status__exact='pending').count()
        return context


def addPackageForm(request):
    context = {'ap': True}
    form = CreatePackageForm(request.POST.copy(), request.FILES)
    if request.method == 'POST':
        form.data['status'] = Package.STATUS[int(request.POST.get('status', 0))][0]
        form.data['is_featured'] = bool(request.POST.get('featured', False))
        if form.is_valid():
            form.save()
            return redirect('package-table')
    context['form'] = form
    context['segment'] = 'form'
    context['active_order'] = Order.objects.filter(status__exact='pending').count()
    return render(request, 'forms/package_form.html', context)


def addAdventureForm(request):
    context = {'ap': True}
    form = CreateAdventureForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            adventure: Adventure = form.save()
            return redirect('package-table')
    context['form'] = form
    context['segment'] = 'form'
    context['active_order'] = Order.objects.filter(status__exact='pending').count()
    return render(request, 'forms/adventure_form.html', context)


def addFoodForm(request):
    context = {'ap': True}
    form = CreateFoodForm(request.POST.copy())
    if request.method == 'POST':
        form.data['breakfast'] = 'false' != request.POST.get('breakfast') != 'unknown'
        form.data['lunch'] = 'false' != request.POST.get('lunch') != 'unknown'
        form.data['snacks'] = 'false' != request.POST.get('snacks') != 'unknown'
        form.data['dinner'] = 'false' != request.POST.get('dinner') != 'unknown'
        if form.is_valid():
            food: Food = form.save()
            return redirect('package-table')
    context['form'] = form
    context['segment'] = 'form'
    context['active_order'] = Order.objects.filter(status__exact='pending').count()
    return render(request, 'forms/food_form.html', context)


def addItineraryForm(request):
    context = {'ap': True}
    form = CreateItineraryForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            itinerary: Itinerary = form.save()
            return redirect('package-table')
    context['form'] = form
    context['segment'] = 'form'
    context['active_order'] = Order.objects.filter(status__exact='pending').count()
    return render(request, 'forms/itinerary_form.html', context)


def addStaffForm(request):
    context = {'ap': True}
    form = CreateUserForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            staff: User = form.save()
            staff.is_staff = True
            staff.set_password(staff.password)
            staff.save()
            return redirect('package-table')
    context['form'] = form
    context['segment'] = 'form'
    context['active_order'] = Order.objects.filter(status__exact='pending').count()
    return render(request, 'forms/staff_form.html', context)


def addCustomerForm(request):
    context = {'ap': True}
    form = CreateUserForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            customer: User = form.save()
            customer.is_customer = True
            customer.set_password(customer.password)
            customer.save()
            return redirect('package-table')
    context['form'] = form
    context['segment'] = 'form'
    context['active_order'] = Order.objects.filter(status__exact='pending').count()
    return render(request, 'forms/customer_form.html', context)


def addPlaceForm(request):
    context = {'ap': True}
    form = CreatePlaceForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            place: Place = form.save()
            print(place)
            return redirect('package-table')
    context['form'] = form
    context['segment'] = 'form'
    context['active_order'] = Order.objects.filter(status__exact='pending').count()
    form.fields['date_time'].widget.attrs['min'] = datetime.now().__str__().split('.')[0]
    return render(request, 'forms/place_form.html', context)


def updatePackageForm(request, identity):
    package = Package.objects.get(id=identity)
    form = None
    if not package:
        redirect('package-table')

    if request.method == 'GET':
        form = CreatePackageForm(initial={
            'name': package.name,
            'type': package.type,
            'itinerary': package.itinerary,
            'price': package.price,
            'desc': package.desc,
            'duration': package.duration,
        })
        return render(request, 'forms/edit_package_form.html',
                      {'ap': True, 'p': package, 'form': form})
    elif request.method == 'POST':
        form = CreatePackageForm(request.POST.copy(), request.FILES, instance=package)
        form.data['status'] = Package.STATUS[int(request.POST.get('status', 0))][0]
        form.data['is_featured'] = bool(request.POST.get('featured', False))
        if form.is_valid():
            form.save()
            return redirect('package-table')

    context = {'ap': True, 'segment': 'form', 'p': package, 'form': form,
               'active_order': Order.objects.filter(status__exact='pending').count()}
    return render(request, 'forms/package_form.html', context)


def updateAdventureForm(request):
    pass


def addOrderForm(request, identity):
    context = {'ap': True}
    form = None
    if identity > 0:
        package = Package.objects.filter(id=identity)[0]
        if package:
            form = CreateOrderForm(initial={'package': package})
    else:
        form = CreateOrderForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            order: Order = form.save()
            return redirect('order-table')
    context['form'] = form
    context['segment'] = 'form'
    context['active_order'] = Order.objects.filter(status__exact='pending').count()
    form.fields['date'].widget.attrs['min'] = date.today()
    return render(request, 'forms/order_form.html', context)


def generate(request):
    user = User.objects.filter(username__exact='Rochak')

    if user:
        print("[WARNING]: DATA HAS ALREADY BEEN GENERATED!")
        return redirect('dashboard')

    if not request.method == "GET" or not GENERATE_DUMMY_DATA:
        return redirect('dashboard')

    staffs = ['Jerry', 'James', 'Json', 'Kate', 'Harry']
    customers = ['Rochak', 'Mahesh', 'Prasesh', 'Nilesh', 'Aayush']
    adventures = [['ABC Trekking', 3], ['EBC Trekking', 3], ['Karnali Rafting', 1]]
    foods = [['Lama Foods', [True, True, False, False]],
             ['Everest FF', [False, True, False, False]],
             ['West Dining', [False, True, False, True]]
             ]
    places = [["Annapurna", 5, "100,100"], ["Namche", 6, "101,101"], ["Jumla", 4, "60,60"]]
    packages = [["Adventurous Annapurna", "Best Value", 120, "Join the Hype", 5, True],
                ["Namche Heights", "Class A", 200, "Join the Hype", 6, True],
                ["West Water", "Economy", 60, "Join the Hype", 4, True]]

    itinerary = [["ABC 5 days", 6], ["EBC 6 days", 7], ["Raft at Karnali 4 days", 5]]

    adventure_objs: [Adventure] = []
    food_objs: [Food] = []
    place_objs: [Place] = []
    itinerary_objs: [Itinerary] = []

    def main():
        generate_customers()
        generate_staff()
        generate_adventure()
        generate_food()
        generate_place()
        generate_itinerary()
        generate_package()

    def generate_customers():
        for customer in customers:
            user = User(username=customer, email=customer.lower() + '@' + customer.lower() + ".com", )
            user.set_password(customer)
            user.is_customer = user.is_active = True
            user.is_staff = user.is_admin = user.is_ban = False
            user.save()

    def generate_staff():
        for staff in staffs:
            user = User(username=staff, email=staff + '@' + staff + ".com", )
            user.set_password(staff)
            user.is_staff = user.is_active = user.is_admin = True
            user.is_customer = user.is_ban = False
            user.save()

    def generate_adventure():
        for a in adventures:
            adv = Adventure(name=a[0], adventure=Adventure.ADVENTURE[a[1]][0])
            adv.save()
            adventure_objs.append(adv)

    def generate_food():
        for f in foods:
            food = Food(name=f[0], breakfast=f[1][0], lunch=f[1][1], snacks=f[1][2], dinner=f[1][3])
            food.save()
            food_objs.append(food)

    def generate_place():
        tz = timezone.now()

        for x in range(len(places)):
            places[x].append(adventure_objs[x])
        for x in range(len(places)):
            places[x].append(food_objs[x])
        for p in places:
            place = Place(name=p[0], coordinate="27.70903097258955,85.32838109540454", date_time=tz)
            place.food = p[4]
            place.save()
            place.adventures.add(p[3])
            place_objs.append(place)

    def generate_itinerary():
        for x in range(3):
            it = Itinerary(name=itinerary[x][0], duration=itinerary[x][1])
            it.save()
            it.places.add(place_objs[x])
            itinerary_objs.append(it)

    def generate_package():
        for x in range(len(packages)):
            packages[x].append(itinerary_objs[x])
        for p in packages:
            pkg = Package(
                name=p[0],
                type=p[1],
                price=p[2],
                desc=p[3],
                duration=p[4],
                is_featured=p[5],
                itinerary=p[6],
                status=Package.STATUS[0][0]
            )
            pkg.save()

    main()
    return redirect('home')
