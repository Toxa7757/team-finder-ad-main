from django import forms
from .models import User
import re

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', 'Пароли не совпадают')

        return cleaned_data

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Приводим к единому стандарту, например, к +7
        if phone.startswith('8'):
            phone = '+7' + phone[1:]
        
        if not re.match(r'^\+7\d{10}$', phone):
            raise forms.ValidationError("Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX")
            
        # Проверка на уникальность (исключая текущего пользователя)
        if User.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            raise forms.ValidationError("Пользователь с таким номером телефона уже существует.")
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and "github.com" not in url:
            raise forms.ValidationError("Ссылка должна вести на домен github.com")
        return url