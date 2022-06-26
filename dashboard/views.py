from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse

from dashboard.config import At as At
from dashboard.models import ActivityLog
from django.views.generic import ListView

from users.models import User
from .forms import CreatePackageForm, CreateStaffForm
from .models import Package, Place


def dashboard(request):
    context = {'segment': 'index', 'ap': At.at()}
    print(context['log'])
    html_template = loader.get_template('dashboard.html')
    return HttpResponse(html_template.render(context, request))


def delete_log(request, identity):
    log = ActivityLog.objects.get(pk=identity)
    if not log:
        messages.error(request, 'Sorry! Something went wrong')
        redirect(reverse('dashboard'), '#zero')
    log.delete()
    messages.success(request, 'Log removed successfully')
    return redirect('dashboard')


def ban_unban_user(request, identity):
    logged_user = request.user

    if logged_user.username == "AnonymousUser":
        messages.error(request, 'User Unauthorized')
        return redirect('dashboard')

    user = User.objects.get(pk=identity)

    if not user:
        messages.error(request, 'Sorry! Something went wrong')
        return redirect('dashboard')
    if user.is_superuser:
        messages.error(request, 'Sorry! You can\'t ban a superuser')
        return redirect('dashboard')

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
    return redirect('dashboard')


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
        'id', 'name', 'is_featured', 'desc').order_by('-id'), 3)

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
        return redirect(request, 'package-table')

    package = Package.objects.filter(id=identity)[0]
    if package:
        messages.success(request, f'Successfully deleted {package.name} package!')
        print(f"Delete {package.name}")
        package.delete()
    else:
        messages.error(request, 'Sorry! Something went wrong.')
    return redirect('package-table')


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
    print(package.status)

    package.save()
    return redirect('package-table')


class GetPackage(ListView):
    model = Package
    template_name = 'tables/package_table.html'
    context_object_name = 'packages'
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super(GetPackage, self).get_context_data(**kwargs)
        context['segment'] = 'tables'
        context['ap'] = At.at()
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
    return render(request, 'forms/package_form.html', context)


def addStaffForm(request):
    context = {'ap': True}
    form = CreateStaffForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            staff: User = form.save()
            staff.is_staff = True
            staff.set_password(staff.password)
            staff.save()
            return redirect('package-table')
    context['form'] = form
    context['segment'] = 'form'
    return render(request, 'forms/staff_form.html', context)


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
        return render(request, 'forms/edit_package_form.html', {'ap': True, 'p': package, 'form': form})
    elif request.method == 'POST':
        form = CreatePackageForm(request.POST.copy(), request.FILES, instance=package)
        form.data['status'] = Package.STATUS[int(request.POST.get('status', 0))][0]
        form.data['is_featured'] = bool(request.POST.get('featured', False))
        if form.is_valid():
            form.save()
            return redirect('package-table')

    context = {'ap': True, 'segment': 'form', 'p': package, 'form': form}
    return render(request, 'forms/package_form.html', context)
