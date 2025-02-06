from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Order

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        unit = request.POST['unit']

        Product.objects.create(name=name, price=price, quantity=0, unit=unit)
        messages.success(request, 'Product added successfully!')
        return redirect('index')

    return render(request, 'add_product.html')

# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Product

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.unit = request.POST.get('unit')
        product.save()
        return redirect('index')  # Redirect to the products list page
    
    return render(request, 'update_product.html', {'product': product})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('index')

def place_order(request):
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        selected_products = []
        total_price = 0

        for product in Product.objects.all():
            quantity = request.POST.get(f'quantity_{product.id}')
            if quantity and int(quantity) > 0:
                quantity = int(quantity)
                total_price += product.price * quantity
                selected_products.append(f"{product.name} ({quantity} {product.unit})")

        if selected_products: 
            Order.objects.create(
                customer_name=customer_name,
                total_price=total_price,
                products=', '.join(selected_products)
            )
            messages.success(request, 'Order placed successfully!')
        else:
            messages.error(request, 'Please select at least one product.')

        return redirect('index')

    products = Product.objects.all()
    return render(request, 'place_order.html', {'products': products})

def orders(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': orders})
