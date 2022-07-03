from django.urls import path
from . import views

urlpatterns = [
    # Mains
    path('', views.Dashboard.as_view(), name="dashboard"),
    path('packages/all/', views.GetAllPackages.as_view(), name="packages"),

    # Add
    path('staff/add/', views.addStaffForm, name="add-staff"),
    path('customer/add/', views.addCustomerForm, name="add-customer"),
    path('place/add/', views.addPlaceForm, name="add-place"),
    path('package/add/', views.addPackageForm, name="add-package"),
    path('adventure/add/', views.addAdventureForm, name="add-adventure"),
    path('food/add/', views.addFoodForm, name="add-food"),
    path('itinerary/add/', views.addItineraryForm, name="add-itinerary"),
    path('order/add/<int:identity>', views.addOrderForm, name="add-order"),

    # Update
    path('package/edit/<int:identity>', views.updatePackageForm, name="update-package"),
    path('adventure/edit/<int:identity>', views.updateAdventureForm, name="update-adventure"),

    # View
    path('packages/', views.GetPackages.as_view(), name="package-table"),
    path('customers/', views.GetCustomers.as_view(), name="customer-table"),
    path('staffs/', views.GetStaffs.as_view(), name="staff-table"),
    path('adventures/', views.GetAdventures.as_view(), name="adventure-table"),
    path('foods/', views.GetFoods.as_view(), name="food-table"),
    path('itineraries/', views.GetItineraries.as_view(), name="itinerary-table"),
    path('places/', views.GetPlaces.as_view(), name="place-table"),
    path('orders/', views.GetOrders.as_view(), name="order-table"),

    # Delete
    path('delete-log/<int:identity>', views.delete_log, name="delete-log"),
    path('package/delete/<int:identity>', views.delete_package, name="del-package"),
    path('adventure/delete/<int:identity>', views.delete_adventure, name="del-adventure"),
    path('food/delete/<int:identity>', views.delete_food, name="del-food"),
    path('itinerary/delete/<int:identity>', views.delete_itinerary, name="del-itinerary"),
    path('place/delete/<int:identity>', views.delete_place, name="del-place"),
    path('account/delete/<int:identity>/<int:redirect_to>', views.delete_account, name="del-account"),

    # Misc
    path('generate/', views.generate, name="generate"),
    path('ban-unban-user/<int:identity>/<int:redirect_to>', views.ban_unban_user, name="ban-unban-user"),
    path('toggle-user-status/<int:identity>/<int:redirect_to>', views.toggle_user_status, name="toggle-user-status"),
    path('packages/feature/<int:identity>', views.featured_package, name="featured-package"),
    path('packages/visibility/<int:identity>', views.hide_unhide_package, name="toggle-package-visibility"),
    path('order/approve/<int:identity>', views.approve_order, name="approve-order"),
    path('order/decline/<int:identity>', views.decline_order, name="decline-order"),
]
