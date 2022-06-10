from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse

from dashboard.config import At as At
from dashboard.models import ActivityLog
from django.views.generic import ListView

from users.models import User, Customer, Staff
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
    log.action = log.ACTION[5][1]
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
        context['customer_count'] = Customer.objects.count()
        context['admin_count'] = User.objects.count() - Customer.objects.count()
        context['package_count'] = Package.objects.filter(status__exact="available").count()
        context['package_count_max'] = Package.objects.all().count()
        context['place_count'] = Place.objects.count()
        context['staff_count'] = Staff.objects.count()

        a_page = self.request.GET.get('a_page', 1)
        c_page = self.request.GET.get('c_page', 1)
        p_page = self.request.GET.get('p_page', 1)

        context['p_admins'] = self.p_admin.page(a_page)
        context['p_customers'] = self.p_customer.page(c_page)
        context['p_packages'] = self.p_package.page(p_page)

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
