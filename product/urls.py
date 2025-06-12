from django.urls import path
from .views import ProductListView
from . import views

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("<int:product_id>/", views.product_detail, name="product_detail"),
]