from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from checkout.models import Order

def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    orders = profile.orders.all()
    classes = False

    for order in orders:
        if order.product.id == 1 or 2:
            classes = True

    template = 'profiles/profile.html'
    context = {
        'orders': orders,
        'classes': classes,
    }

    return render(request, template, context)


@login_required
def short_stories(request):
    """ A view to return the short stories page """
    profile = get_object_or_404(UserProfile, user=request.user)

    orders = profile.orders.all()

    for order in orders:
        if order.product.id == 4:

            template = 'profiles/short_stories.html'
            context = {
                'orders': orders,
            }
            return render(request, template, context)

    messages.error(request, "Sorry! You don't have authorisation to view that page.")
    return render(request, 'profiles/profile.html')




@login_required
def recorded_lessons(request):
    """ A view to return the recorded lessons page """
    profile = get_object_or_404(UserProfile, user=request.user)

    orders = profile.orders.all()

    for order in orders:
        if order.product.id == 3:

            template = 'profiles/recorded_lessons.html'
            context = {
                'orders': orders,
            }
            return render(request, template, context)

    messages.error(request, "Sorry! You don't have authorisation to view that page.")
    return render(request, 'profiles/profile.html')


