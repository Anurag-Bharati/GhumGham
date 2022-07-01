from django.urls import path
from . import views

urlpatterns = [
    # Mains
    path('', views.Dashboard.as_view(), name="dashboard"),

    # Add
    path('staff/add/', views.addStaffForm, name="add-staff"),
    path('customer/add/', views.addCustomerForm, name="add-customer"),
    path('place/add/', views.addPlaceForm, name="add-place"),
    path('package/add/', views.addPackageForm, name="add-package"),
    path('adventure/add/', views.addAdventureForm, name="add-adventure"),
    path('food/add/', views.addFoodForm, name="add-food"),
    path('itinerary/add/', views.addItineraryForm, name="add-itinerary"),

    # Update
    path('package/edit/<int:identity>', views.updatePackageForm, name="update-package"),

    # View
    path('packages/', views.GetPackage.as_view(), name="package-table"),

    # Delete
    path('delete-log/<int:identity>', views.delete_log, name="delete-log"),
    path('packages/delete/<int:identity>', views.delete_package, name="del-package"),

    # Misc
    path('generate/', views.generate, name="generate"),
    path('ban-user/<int:identity>', views.ban_unban_user, name="ban-unban-user"),
    path('packages/feature/<int:identity>', views.featured_package, name="featured-package"),
    path('packages/visibility/<int:identity>', views.hide_unhide_package, name="toggle-package-visibility"),
]
