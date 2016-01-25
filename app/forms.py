'''
Created on 2015. 11. 28.

@author: daein
'''

from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from app.models import Post
from django.contrib.auth.forms import UserCreationForm


class Postwrite(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'posts', 'tags',)
        
        
class CreateUser(UserCreationForm):
    
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user