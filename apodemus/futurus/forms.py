from futurus.models import Person
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('email', 'password')

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'pic', 'story', 'hometown', 'twitter', 'facebook_url', 'wiki_url')

