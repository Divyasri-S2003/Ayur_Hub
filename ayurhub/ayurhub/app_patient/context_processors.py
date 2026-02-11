from .models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        # Get total number of unique items in the cart for the user
        count = Cart.objects.filter(patient=request.user).count()
        return {'global_cart_count': count}
    return {'global_cart_count': 0}