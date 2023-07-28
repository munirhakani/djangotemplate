from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings

from .forms import UserCreationForm, UserChangeForm, SetPasswordForm, ResendLinkForm
from .token import account_activation_token

from django.contrib.auth import get_user_model
User = get_user_model()
# from django.contrib.auth.models import User


def tokengenerator(request, user):
    current_site = get_current_site(request)
    domain = current_site.domain if settings.DEBUG else current_site.domain[:-5]
    subject = f'Activate your {domain} account.'
    message = render_to_string('email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        tokengenerator(request, user)
        messages.success(request, f'Your account has been created. Activation link has been sent to email.')
        return redirect('nothing')
    context = {'legend': 'Register Today', 'form': form, 'button': 'Register & Send a link', }
    return render(request, 'form.html', context)


from django.contrib.auth.models import Permission
def activate(request, uidb64, token):
    user = User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
    if account_activation_token.check_token(user, token):
        user.is_active = True
        list = (
            'Can view family', 'Can add family', 'Can change family',
            'Can view person', 'Can add person', 'Can change person',
        )
        user.user_permissions.set(Permission.objects.filter(name__in=list))
        user.save()
        login(request, user)
        messages.success(request, (f'Your account have been successfully activated. You are logged in.'))
        return redirect('/')
    else:
        messages.warning(request, (f'The confirmation link was invalid, possibly because it has already been used.'))
        return redirect('login')


@login_required
def profile(request):
    form = UserChangeForm(instance=request.user)
    if request.POST:
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account profile has been updated!')
    context = {'legend': 'Update Profile', 'form': form, 'button': 'Update', }
    return render(request, 'form.html', context)


@login_required
def password(request):
    form = SetPasswordForm(user=request.user)
    if request.POST:
        form = SetPasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Your account password has been updated!')
    context = {'legend': 'Update Password', 'form': form, 'button': 'Update', }
    return render(request, 'form.html', context)


def resendlink(request):
    form = ResendLinkForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            tokengenerator(request, user)
            messages.success(request, f'Activation link has been re-sent to email.')
            return redirect('nothing')
    context = {'legend': 'Resend activation link', 'form': form, 'button': 'Send a link', }
    return render(request, 'form.html', context)


# #######################################################################################
# from django import forms

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# class ProfileForm(forms.ModelForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']

# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views import View

# class RegisterView(View):
#     form_class = UserRegistrationForm
#     template_name = 'register.html'
#     success_message = f'Your account has been created! You are now able to log in.'
    
#     def get(self, request):
#         return render(request, self.template_name, {'form': self.form_class})
    
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, self.success_message)
#             return redirect('login')
#         return render(request, self.template_name, {'form': form})

# class ProfileView(LoginRequiredMixin, View):
#     form_class = ProfileForm
#     template_name = 'profile.html'
#     success_message = f'Your profile has been updated!'

#     def get(self, request):
#         return render(request, self.template_name, {'form': self.form_class(instance=request.user)})
    
#     def post(self, request):
#         form = self.form_class(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, self.success_message)
#             return redirect('profile')
#         return render(request, self.template_name, {'form': form})