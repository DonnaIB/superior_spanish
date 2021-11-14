from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from profiles.models import UserProfile
from checkout.models import Order
from .forms import ProductForm
# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('home'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

            if not products:
                messages.info(request, "Sorry there is nothing matching your search criteria!")
                return redirect(reverse('home'))

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_info(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:

        profile = get_object_or_404(UserProfile, user=request.user)
        
        orders = profile.orders.all()
        stories = False
        lessons = False

        for order in orders:
            if order.product.id == 3:
                print("3")
                lessons = True

            elif order.product.id == 4:
                print("4")
                stories = True


        context = {
            'product': product,
            'orders': orders,
            'lessons': lessons,
            'stories': stories

        }

        return render(request, 'products/product_info.html', context)

    context = {
        'product': product,
        }

    return render(request, 'products/product_info.html', context)


def add_product(request):
    """ Add a product """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Your new product has been added!')
            return redirect(reverse('product_info', args=[product.id]))
        else:
            messages.error(request, 'Product not added. Please check the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
