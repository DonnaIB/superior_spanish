from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from checkout.models import Order

def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    orders = profile.orders.all()
    classes = False

    for order in orders:
        if order.product.id == 1 or 2:
            print("class")
            classes = True

    template = 'profiles/profile.html'
    context = {
        'orders': orders,
        'classes': classes,
    }

    return render(request, template, context)

def short_stories(request):
    """ A view to return the short stories page """

    return render(request, 'profiles/short_stories.html')


def recorded_lessons(request):
    """ A view to return the recorded lessons page """

    return render(request, 'profiles/recorded_lessons.html')
