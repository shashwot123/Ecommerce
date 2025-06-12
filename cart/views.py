from django.shortcuts import get_object_or_404, redirect, render
from product.models import Product

def add_to_cart(request, product_id):
    #get existing cart from session or initialize an empty cart
    cart = request.session.get("cart", {})

    #fetch from database using product_id
    #to avoid crash if product_id not found
    product = get_object_or_404(Product, id = product_id)

    #session keys must be strings apparently
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str]["quantity"] += 1
    else:
        cart[product_id_str] = {
            "name": product.name,
            "price": float(product.price),
            "image": product.image.url,
            "quantity": 1,
            "subtotal": float(product.price)
        }
    
    cart[product_id_str]["subtotal"] = cart[product_id_str]["price"]*cart[product_id_str]["quantity"]

    #save updated cart to session
    request.session["cart"] = cart

    request.session.modified = True

    return redirect("cart_detail")

def cart_detail(request):
    cart = request.session.get("cart", {})

    return render(request, "cart/cart_detail.html",{
        "cart": cart,
    })


