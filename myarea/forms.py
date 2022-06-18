from django import forms
from .models import *


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user']

class UserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields ='__all__'


class CreateHoodForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood
        fields ='__all__'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields ='__all__'


class BusinessForm(forms.ModelForm):
    class Meta:
        model  = Business
        fields ='__all__'