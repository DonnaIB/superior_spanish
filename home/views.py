from django.shortcuts import render, get_object_or_404
from products.models import Product, Category

# Create your views here.

def index(request):
    """ A view to return the index page """
    
    products = Product.objects.all()
    query = None
    categories = None


    context = {
        'products': products,
    }

    return render(request, 'home/index.html', context)