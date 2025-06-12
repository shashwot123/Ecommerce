from django.views.generic import ListView
from .models import Product
from django.shortcuts import render, get_object_or_404

class ProductListView(ListView):
    model = Product
    template_name = "product/product_list.html"
    paginate_by = 3

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product/product_detail.html",{
        "product" : product
    })
