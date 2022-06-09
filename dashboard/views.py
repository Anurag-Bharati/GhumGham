from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import loader
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


class Dashboard(ListView):
    model = ActivityLog
    template_name = 'dashboard.html'
    context_object_name = 'logs'
    paginate_by = 4
    ordering = '-id'
    page_kwarg = "page_log"

    p_admin = Paginator(User.objects.filter(is_superuser=True).values('username', 'created_date').order_by("-id"), 3)
    p_customer = Paginator(User.objects.filter(is_customer=True).values('username', 'created_date').order_by("-id"), 3)
    p_package = Paginator(Package.objects.values('name', 'desc').order_by('-id'), 3)

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['segment'] = 'index'
        context['ap'] = At.at()
        context['user_count'] = User.objects.count()
        context['customer_count'] = Customer.objects.count()
        context['admin_count'] = User.objects.count() - Customer.objects.count()
        context['package_count'] = Package.objects.filter(status__exact="available").count()
        context['place_count'] = Place.objects.count()
        context['staff_count'] = Staff.objects.count()

        a_page = self.request.GET.get('a_page', 1)
        c_page = self.request.GET.get('c_page', 1)
        p_page = self.request.GET.get('p_page', 1)

        context['p_admins'] = self.p_admin.page(a_page)
        context['p_customers'] = self.p_customer.page(c_page)
        context['p_packages'] = self.p_package.page(p_page)

        return context
