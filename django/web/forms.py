from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import web.models

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class RatingForm(forms.ModelForm):    
    class Meta:
        model = web.models.Rating
        fields = "__all__"
        exclude = ["user", "site"]
        