from django.urls import reverse
from .utils import token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib import messages, auth
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import User
from .forms import UserForm
from django.views import View

def index(request):
    return HttpResponse("<h1>Landing Page</h1>")


class RegisterationView(View):
    
    def get(self, request):
        form = UserForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('accounts:activate', kwargs={
                    'uidb64': uidb64, 'token': token_generator.make_token(user)})

                activate_url = f'http://{domain}{link}'
                
                email_body = f'Here is your activation link:\n{activate_url}'

                send_mail(
                    'Account Activation Email',
                    email_body,
                    'noreply@semicolon.com',
                    [user.email],
                    fail_silently=False,
                )
                return redirect('accounts:landing')
            else:
                return render(request, 'accounts/register.html', {'form': form})


def createUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email_body = ''
            send_mail(
                'Account Activation Email',
                email_body,
                'noreply@semicolon.com',
                [user.email],
                fail_silently=False,
            )
        else:
            return render(request, 'accounts/register.html', {'form': form})

    form = UserForm()
    return render(request, 'accounts/register.html', {'form': form})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('accounts:login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('accounts:login')
            user.is_active = True
            user.save()
            return redirect('accounts:login')

        except Exception as ex:
            pass

        return redirect('accounts:login')


class UserLoginView(LoginView):

    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if not user:
                messages.error(request, 'Invalid credentials or email not verified yet')
                return render(request, 'accounts/login.html')
            else:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('accounts:landing')
                else:
                    messages.error(request, 'Account is not active,please check your email')
                    return render(request, 'accounts/login.html')

        else:
            messages.error(request, 'Please fill all fields')
            return render(request, 'accounts/login.html')


class UserLogoutView(View):
    def get(self, request):
        auth.logout(request)
        print("logged out")
        return redirect('accounts:login')

    def post(self, request):
        auth.logout(request)
        print("logged out")
        return redirect('accounts:login')
    