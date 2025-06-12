from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    #the default django signup form doesnot have a email field
    #so adding it explicitly 
    email = forms.EmailField(required=True)

    #to provide metadata to the form like what model to use and fields to include
    class Meta:
        #built-in User model
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        #call the UserCreationForm's save() method but not save it yet
        user = super().save(commit=False)
        #add email to the user
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user