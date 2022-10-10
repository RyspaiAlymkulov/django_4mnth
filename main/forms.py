from django import forms
from django.core.exceptions import ValidationError

from .models import Film, Review
from django.contrib.auth.models import User


class FilmCreateForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = 'title link producer rating duration'.split()
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'link': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'producer': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'rating': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'duration': forms.TimeInput(attrs={
                'class': 'form-control'
            }),
        }


class UserCreateForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise ValidationError('Уже есть такой пользователь')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        password1 = self.cleaned_data['password1']
        if password != password1:
            raise ValidationError('Не совпадают')
        return password1


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

