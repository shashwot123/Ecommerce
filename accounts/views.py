from django.views.generic.edit import FormView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render

def home(request):
    return render(request, "home.html")

#View for Signup
class SignupView(FormView):
    template_name = "registration/signup.html"
    #form_class is used in FormView
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")

    #overriding form_valid() to automatically login the user after signup
    def form_valid(self, form):
        #calling the CustomUserCreationForm's save function 
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

