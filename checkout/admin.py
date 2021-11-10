from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):

    readonly_fields = ('order_number', 'date',)

    fields = ('order_number', 'date', 'first_name',
              'last_name',
              'email',
              'country',
              'product',
              'total',)

    list_display = ('order_number', 'date', 'first_name',
                    'last_name',
                    'email',
                    'country',
                    'total',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)
