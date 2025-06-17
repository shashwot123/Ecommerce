from django.shortcuts import get_object_or_404, redirect, render
from product.models import Product
from django.views.decorators.http import require_POST
from .models import Cart, CartItem

@require_POST
def add_to_cart(request, product_id):
    #fetch from database using product_id
    #to avoid crash if product_id not found
    product = get_object_or_404(Product, id = product_id)
    
    try:
        quantity = max(1, int(request.POST.get("quantity", 1)))
    except (ValueError, TypeError):
        quantity = 1

    if request.user.is_authenticated:
        #get cart if the user has an active cart, else create one
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)

        #get item if it is in the cart, else create one with default values
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                "quantity": quantity,
                "price_at_addition": product.price
            }
        )
        #if item is in the cart, update quantity
        if not created:
            item.quantity += quantity
            item.save()

    else:
        #get existing cart from session or initialize an empty cart
        cart = request.session.get("cart", {})

        #session keys must be strings
        product_id_str = str(product_id)

        #return existing item if it exists, else create item with the values
        item = cart.setdefault(product_id_str, {
            "name": product.name,
            "price": float(product.price),
            "image": product.image.url,
            "quantity": 0,
        })
        item["quantity"] += quantity
        item["subtotal"] = round(item["price"]*item["quantity"],2)

        #save updated cart to session
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart_detail")

@require_POST
def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        #get product and cart
        product = get_object_or_404(Product, id=product_id)
        cart = get_object_or_404(Cart, user=request.user, is_active=True)

        #delete if item exists in cart
        item = get_object_or_404(CartItem, cart=cart, product=product)
        item.delete()

    else:
        cart = request.session.get("cart", {})
        
        #session keys must be strings
        product_id_str = str(product_id)

        #delete item if it exixts in cart
        cart.pop(product_id_str, None)
        
        #update the session
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart_detail")

@require_POST
def update_cart_quantity(request, product_id):
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 1
    
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart = get_object_or_404(Cart, user=request.user, is_active=True)
        item = get_object_or_404(CartItem, cart=cart, product=product)
        
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

    else:
        cart = request.session.get("cart", {})
        product_id_str = str(product_id)

        if quantity <= 0:
            cart.pop(product_id_str, None)
        else:
            if product_id_str in cart:
                item = cart[product_id_str]
                item["quantity"] = quantity
                item["subtotal"] = round(item["price"]*item["quantity"],2)
        
        #update the session
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart_detail")    

def cart_detail(request):
    cart_items = []
    total = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if cart:
            for item in cart.items.all():
                cart_items.append({
                    "product_id": item.product.id,
                    "name": item.product.name,
                    "image": item.product.image.url,
                    "quantity": item.quantity,
                    "subtotal": float(item.subtotal),
                    "price": float(item.price_at_addition)
                })
            total = float(cart.total)
    else:
        cart = request.session.get("cart", {})
        for product_id_str, item in cart.items():
            subtotal = float(item["price"]*item["quantity"])
            cart_items.append({
                    "product_id": int(product_id_str),
                    "name": item["name"],
                    "image": item["image"],
                    "quantity": item["quantity"],
                    "subtotal": round(subtotal,2),
                    "price": float(item["price"])
                })
            total += subtotal

    #cart_items is a dict with the same keys whether logged in user or guest user
    return render(request, "cart/cart_detail.html",{
        "cart_items": cart_items,
        "total": round(total,2),
    })


