from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name="dashboard"),
    path('package/add/', views.addPackageForm, name="add-package"),
    path('staff/add/', views.addStaffForm, name="add-staff"),
    path('package/edit/<int:identity>', views.updatePackageForm, name="update-package"),
    path('packages/', views.GetPackage.as_view(), name="package-table"),
    path('packages/delete/<int:identity>', views.delete_package, name="del-package"),
    path('packages/feature/<int:identity>', views.featured_package, name="featured-package"),
    path('packages/visibility/<int:identity>', views.hide_unhide_package, name="toggle-package-visibility"),
    path('delete-log/<int:identity>', views.delete_log, name="delete-log"),
    path('ban-user/<int:identity>', views.ban_unban_user, name="ban-unban-user"),
]
