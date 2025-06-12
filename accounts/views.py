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
    #resolve url when accessed
    success_url = reverse_lazy("product_list")

    #overriding form_valid() to automatically login the user after signup
    #only runs when all data is valid when the user submits the form
    def form_valid(self, form):
        #calling the CustomUserCreationForm's save function 
        user = form.save()
        login(self.request, user)
        #call the form_valid() method from FormView for next steps and redirect
        return super().form_valid(form)

