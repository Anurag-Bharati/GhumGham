from django.shortcuts import redirect

def has_session(func):
    def wrapper_function(request, *args, **kwargs):
        if not request.user:
            redirect("auth")
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return func(request, *args, **kwargs)
    return wrapper_function


def admin_only(func):
    def wrapper_function(request, *args, **kwargs):
        if not request.user:
            redirect("auth")
        if request.user.is_staff or request.user.is_superuser or request.user.is_admin:
            return func(request, *args, **kwargs)
        elif not request.user.is_staff or not request.user.is_superuser:
            return redirect('/')
    return wrapper_function

