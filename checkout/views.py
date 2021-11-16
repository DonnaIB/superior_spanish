from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from products.models import Product
from profiles.models import UserProfile
import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)

def checkout(request, product_id):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.user.is_authenticated:
        if request.method == 'POST':
            product = get_object_or_404(Product, pk=product_id)


            form_data = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'country': request.POST['country'],
            }
            
            order_form = OrderForm(form_data)
    
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.product = product
                order.total = order.product.price
                order.save()

                profile = UserProfile.objects.get(user=request.user)
                order.user_profile = profile
                order.save()

                messages.success(
                    request, 'Your new purchase has been made successfully.')

                return redirect('/profile')
            
        else:
            
            product = get_object_or_404(Product, pk=product_id)
            order_form = OrderForm()
            total = product.price
            stripe_total = round(total * 100)
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                    amount=stripe_total,
                    currency=settings.STRIPE_CURRENCY,
            )

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'product': product,
        }

        return render(request, template, context)
 
    messages.info(request, 'Please log in before purchasing')

    return redirect(reverse('account_login'))

