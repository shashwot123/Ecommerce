from django.urls import path
from accounts.views import SignupView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    #.as_view() converts class based view into a callable view
    path("signup/", SignupView.as_view(), name="signup"),
    #using django's LoginView
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]