from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'executed', 'first_name', 'phoneNumber', 'email',
                    'city', 'delivery', 'address', 'comment',
                    'created', 'updated', 'paymentMethod', 'paid']
    list_filter = ['paid', 'executed', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)