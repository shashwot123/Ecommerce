from django.urls import path
from accounts.views import SignupView

urlpatterns = [
    #.as_view() converts class based view into a callable view
    path("signup/", SignupView.as_view(), name="signup")
]