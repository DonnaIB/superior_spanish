from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('<product_id>', views.checkout, name='checkout'),
    path('wh/', webhook, name='webhook'),
]
