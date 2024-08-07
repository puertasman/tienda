from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

def inicio(request):
    return render(request, 'shop/inicio.html')

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(parent=None)  # Solo categorías de nivel superior
    products = Product.objects.filter(available=True)
    current_category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        current_category = category
        category_ids = [category.id]  # Comienza con la categoría principal

        subcategories = category.children.all()
        category_ids.extend(subcategories.values_list('id', flat=True))

        products = Product.objects.filter(category__id__in=category_ids, available=True)

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'current_category': current_category
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    has_parent = product.category.parent is not None if product.category else False
    form = CartAddProductForm(max_quantity=product.inventory)  # Asegúrate de pasar max_quantity correctamente

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'has_parent': has_parent,
        'form': form  
    })    
