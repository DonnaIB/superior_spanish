from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
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
    return render(request, 'profiles/recorded_lessons.html')    

@login_required
def recorded_lessons(request):
    """ A view to return the recorded lessons page """

    return render(request, 'profiles/recorded_lessons.html')
