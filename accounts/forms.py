from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    #the default django signup form doesnot have a email field
    # so adding it explicitly 
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded px-3 py-2',
            })

    class Meta:
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