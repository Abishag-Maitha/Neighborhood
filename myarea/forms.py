from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


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

class BusinessForm(forms.ModelForm):
    class Meta:
        model  = Business
        fields ='__all__'

class RegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']

    def save(self, commit=True):
        user=super().save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:

            user.save()
        return user

class profileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['profile_picture', 'bio', 'location']