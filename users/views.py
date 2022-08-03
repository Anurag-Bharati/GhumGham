import re
import threading

import validate_email as EmailValidator

from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as django_login, user_logged_out
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from GhumGham import settings
from users.forms import LoginForm, RegistrationForm
from users.models import User
from users.utils import activation_token
from modules.ghumgham_krypto import Krypto

otp = None
otp_user = None


# handles login and register
def authenticate(request):
    # clear notice
    messages.error(request, "")
    if request.method == 'POST':
        if 'email' not in request.POST:
            return login(request)
        return signup(request)
    return render(request, './authentication.html')


def checkPin(request, pin):
    pin1 = request.POST.get('digit-1', 0)
    pin2 = request.POST.get('digit-2', 0)
    pin3 = request.POST.get('digit-3', 0)
    pin4 = request.POST.get('digit-4', 0)
    pin5 = request.POST.get('digit-5', 0)
    pin6 = request.POST.get('digit-6', 0)
    user_pin: int = pin1 + pin2 + pin3 + pin4 + pin5 + pin6
    return pin == user_pin


verf = None
forget_email = None


def forget_pass(request):  # Dummy Logic TODO Actual
    global verf, forget_email
    if request.method == "GET":
        return render(request, './forget-password.html')
    elif request.method == "POST":
        if not forget_email:
            forget_email = request.POST.get('email', "")
        if not verf:
            verf = request.POST.get('digit-1', 0)
        if verf:
            context = {'email': forget_email, 'enable': True}
            return render(request, './forget-password.html', context)
        if forget_email:
            context = {'email': forget_email}
            return render(request, './forget-password.html', context)

        messages.error(request, "Please provide a valid email")
        return render(request, './forget-password.html')


def otp_login(request):
    global otp
    if request.method == "GET":
        return render(request, './otp-login.html')

    elif request.method == "POST":
        global otp_user
        email = request.POST.get('email', "")
        if not otp:
            otp = Krypto.generate(6)
            print(otp)

        if email:
            try:
                otp_user = User.objects.get(email__exact=email)
                print('nice')
            except Exception as e:
                print('[DatabaseQueryException] @users.views "User not found by email", line 87 | Response = ' +
                      str(e))
                return render(request, 'otp-login.html')
            if otp_user:
                context = {'email': email}
                email_context = render_to_string('./email/login-otp.html',
                                                 {'user': otp_user.username, "code": otp})
                text_content = strip_tags(email_context)

                mail = EmailMultiAlternatives(
                    "Your Login OTP",
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                mail.attach_alternative(email_context, "text/html")

                Thread(mail).start()
                return render(request, 'otp-login.html', context)

        else:
            if checkPin(request, otp):
                otp = None
                django_login(request, otp_user, backend=settings.AUTHENTICATION_BACKENDS[0])
                messages.success(request, "Successfully signed in as " + request.user.username)
                return redirect('home')
            else:
                messages.error(request, "Invalid OTP Code. Please Retry")
                return render(request, './otp-login.html', {'email': " "})


def verification(request, identity, token):  # pragma: no cover
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(identity)))
            if user.is_active:
                messages.error(request, "Account has already been activated")
                return redirect("auth")

            elif activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Your account has been successfully activated')
                return redirect('activated')

            return redirect('activated')

        except Exception as ex:
            print(ex)
            return redirect('auth')


def activated(request):  # pragma: no cover
    return render(request, './activated.html')


# basic password check using regex
def checkPass(request, password):
    if len(password) < 6:
        if request:
            messages.error(request, 'Password too short')
        return True
    elif not re.search("[a-z]", password):
        if request:
            messages.error(request, 'Password must contain small letters')
        return True
    elif not re.search("[A-Z]", password):
        if request:
            messages.error(request, 'Password must contain capital letters')
        return True
    elif not re.search("[0-9]", password):
        if request:
            messages.error(request, 'Password must contain number')
        return True
    return False


def login(request):
    form = LoginForm(request.POST)

    if not form.is_valid():
        messages.error(request, "Please fill all the forms.")
        return render(request, './authentication.html', status=400)

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    user = auth.authenticate(username=username, password=password)
    context = {
        'fieldValues': request.POST,
        'signUp': False
    }

    # Database checks
    if not user:
        try:
            user_temp = User.objects.get(username=username)
        except Exception as e:
            print('[DatabaseQueryException] @users.views "User not found", line 87 | Response = ' + str(e))
            user_temp = None

        if user_temp is None:
            messages.error(request, "Account does not exists, Please create one.")
            return render(request, './authentication.html', status=400)
        elif not user_temp.check_password(password):
            messages.error(request, "Password doesn't match")
            return render(request, './authentication.html', context, status=400)
        else:
            messages.error(request, "Account not activated, Please check your email.")
            return render(request, './authentication.html', context, status=400)

    # ban check
    if user.is_ban:
        messages.error(request, "Account is banned, Please contact an Admin.")
        return render(request, './authentication.html', context, status=400)
    auth.login(request, user)
    messages.success(request, "Successfully signed in as " + request.user.username)

    # authorization
    if request.user.is_staff:
        return redirect('dashboard')
    return redirect('home')


def signup(request):
    context = {
        'fieldValues': request.POST,
        'signUp': True
    }
    form = RegistrationForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please fill all the forms.")
        return render(request, './authentication.html', context, status=400)

    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    address = request.POST['address']

    # Guard Clauses
    if User.objects.filter(username=username).exists():
        messages.error(request, 'Username already taken!')
        return render(request, './authentication.html', context, status=400)
    elif User.objects.filter(email=email).exists():
        messages.error(request, 'Email already exists')
        return render(request, './authentication.html', context, status=400)
    elif not EmailValidator.validate_email(email):
        messages.error(request, 'Invalid Email')
        return render(request, './authentication.html', context, status=400)
    elif checkPass(request, password):
        return render(request, './authentication.html', context, status=400)
    else:

        # once the data is valid create user
        user = User.objects.create_user(username=username, email=email, address=address)
        user.set_password(password)
        user.is_active = user.is_staff = user.is_admin = False
        user.is_customer = True
        user.save()
        current_site = get_current_site(request).domain

        magic_link = reverse('activate', kwargs={
            'identity': urlsafe_base64_encode(force_bytes(user.pk)), 'token': activation_token.make_token(user)})
        activate_url = 'http://' + current_site + magic_link

        email_context = render_to_string('./email/verification.html',
                                         {'user': user.username, "activator": activate_url})
        text_content = strip_tags(email_context)

        mail = EmailMultiAlternatives(
            "Activate your account",
            text_content,
            settings.EMAIL_HOST_USER,
            [email]
        )
        mail.attach_alternative(email_context, "text/html")

        Thread(mail).start()
        messages.success(request, 'A verification mail is sent to your email')
        return render(request, './authentication.html', context)


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


def logout(request):
    global otp_user, otp
    otp_user = None
    otp = None
    messages.success(request, f"{request.user.username} Logged out successfully")

    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated:
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)

    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

    # clear msg
    storage = messages.get_messages(request)
    storage.used = True
    return redirect('auth')


