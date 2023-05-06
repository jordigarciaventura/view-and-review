from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import web.models

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'E-mail'}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat password'
    
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
        hidden = ['film']
        exclude = ['user', 'reputation']
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RatingForm, self).__init__(*args, **kwargs)
        self.fields['review'].widget = forms.Textarea(attrs={'rows':'5'})
        self.fields['review'].widget.attrs['class'] = 'form-control'
        self.fields['review'].widget.attrs['placeholder'] = 'lorem ipsum'
        self.fields['review_title'].widget.attrs['class'] = 'form-control'
        self.fields['review_title'].widget.attrs['placeholder'] = 'lorem ipsum'
        
class ReputationForm(forms.ModelForm):
    class Meta:
        model = web.models.Reputation
        fields = "__all__"
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(ReputationForm, self).__init__(*args, **kwargs)
