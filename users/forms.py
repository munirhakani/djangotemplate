from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.core.exceptions import ValidationError
User = get_user_model()


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', ]

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError('A user with that email address already exists.')
        return self.cleaned_data['email']


class UserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['username'].widget.attrs['onfocus'] = 'this.setSelectionRange(0, this.value.length)'

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exclude(id=self.instance.pk).exists():
            raise ValidationError('A user with that email address already exists.')
        return self.cleaned_data['email']


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['password1', 'password2', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['new_password1'].widget.attrs['onfocus'] = 'this.setSelectionRange(0, this.value.length)'


class ResendLinkForm(forms.Form):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['email', ]