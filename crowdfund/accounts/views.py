from django.contrib.auth.hashers import check_password
from django.urls import reverse, reverse_lazy
from projects.models import Project, Donation
from .utils import token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from .models import User
from .forms import ProfileUpdateForm, UserForm, LoginForm
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget



def landing(request):
    return redirect('accounts:login')


class RegisterationView(View):
    
    def get(self, request):
        form = UserForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES)
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
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm


class UserLogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('accounts:login')


def profile(request):
    return redirect('accounts:profile', request.user.pk)


class ProfileView(DetailView):
    model = User
    template_name = 'accounts/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_projects = Project.objects.filter(user=context['user']).order_by('-start_time')[:2]
        context['user_projects'] = user_projects
        return context


class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    # fields = ('first_name', 'last_name', 'username', 'phone_number', 'profile_picture', 'birth_date', 'country', 'facebook')
    

class ProfileDeleteView(DeleteView):
    model = User
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('accounts:login')

    def post(self, request, *args, **kwargs):
        form_password = request.POST.get('password')
        user_password = request.user.password
        if check_password(form_password, user_password):
            return self.delete(request, *args, **kwargs)
        messages.error(self.request, 'Incorrect password!')
        return redirect('accounts:profile_delete', self.kwargs['pk'])


class UserProjects(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        queryset = self.model.objects.filter(user=user)
        return queryset


class UserDonations(ListView):
    model = Donation
    template_name = 'accounts/user_donations.html'
    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        queryset = self.model.objects.filter(user=user).order_by('-created')
        return queryset


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password/password_reset.html", context={"form":password_reset_form})
