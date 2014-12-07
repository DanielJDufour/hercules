from futurus.models import Facebook, LinkedIn, Person, Twitter, Wiki
from django.contrib.auth.models import User
from django import forms

class CreateOrgForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    abbreviation = forms.CharField(max_length=10, required=False)
    logo = forms.ImageField(required=False)
    organization_created = forms.DateField(required=False)
    facebook = forms.URLField(max_length=200, required=False)
    linkedin = forms.URLField(max_length=200, required=False)
    mission = forms.CharField(max_length=10000, required=False)
    twitter = forms.CharField(max_length=200, required=False)
    wiki = forms.URLField(required=False)


class EditPersonForm(forms.Form):
    facebook = forms.URLField(max_length=200, required=False)
    hometown = forms.CharField(max_length=200, required=False)
    linkedin = forms.URLField(max_length=200, required=False)
    name = forms.CharField(max_length=200, required=True)
    pic = forms.ImageField(required=False)
    story = forms.CharField(max_length=10000, required=False)
    twitter = forms.CharField(max_length=200, required=False)
    wiki = forms.URLField(required=False)

class FacebookForm(forms.ModelForm):
    class Meta:
        model = Facebook
        fields = ('url',)

class LinkedInForm(forms.ModelForm):
    class Meta:
        model = LinkedIn
        fields = ('url',)

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'pic', 'story', 'hometown',)

class TwitterForm(forms.ModelForm):
    class Meta:
        model = Twitter
        fields = ('url',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('email', 'password',)

class WikiForm(forms.ModelForm):
    class Meta:
        model = Wiki
        fields = ('url',)
