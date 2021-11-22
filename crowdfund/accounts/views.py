from django.http.response import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from .forms import UserForm
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from .utils import token_generator
from django.contrib import messages
from django.contrib.auth.views import LoginView


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

        return redirect('login')


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    