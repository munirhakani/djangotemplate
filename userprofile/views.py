from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.base import View
from users.forms import UserCreationForm, UserChangeForm
from users.views import tokengenerator
from userprofile.forms import ProfileForm


class UserCreationView(View):
    template_name = 'userprofile/form.html'
    form_class = UserCreationForm
    legend = 'Register Today'
    button = 'Register & Send a link'
    
    def get(self, request):
        context = {
            'form': self.form_class(),
            'formProfile': ProfileForm(),
            'legend': self.legend,
            'button': self.button,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        formProfile = ProfileForm(request.POST)
        if form.is_valid() and formProfile.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            formProfile = ProfileForm(request.POST, instance=user.profile)
            formProfile.save()
            tokengenerator(request, user)
            messages.success(request, f'Your account has been created. Activation link has been sent to email.')
            return redirect('nothing')
        context = {
            'form': form,
            'formProfile': formProfile,
            'legend': self.legend,
            'button': self.button,
        }
        return render(request, self.template_name, context)


class UserProfileView(View):
    template_name = 'userprofile/form.html'
    form_class = UserChangeForm
    legend = 'Update Profile'
    button = 'Update'
    
    def get(self, request):
        context = {
            'form': self.form_class(instance=request.user),
            'formProfile': ProfileForm(instance=request.user.profile),
            'legend': self.legend,
            'button': self.button,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        formProfile = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid() and formProfile.is_valid():
            form.save()
            formProfile.save()
            messages.success(request, f'Your profile has been updated!')
        context = {
            'form': form,
            'formProfile': formProfile,
            'legend': self.legend,
            'button': self.button,
        }
        return render(request, self.template_name, context)