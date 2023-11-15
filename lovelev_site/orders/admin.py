from __future__ import unicode_literals
from django.http import HttpResponse
import csv
import datetime
from django.contrib import admin
from .models import Order, OrderItem


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; \
        filename=Report on orders-{}.csv'.format(datetime.datetime.now().strftime("%d/%m/%Y"))
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Первая строка- оглавления
    writer.writerow([field.verbose_name for field in fields])
    # Заполняем информацией
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Экспорт в CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'executed', 'first_name', 'phoneNumber', 'email',
                    'city', 'delivery', 'address', 'comment',
                    'created', 'updated', 'paymentMethod', 'paid']
    list_filter = ['paid', 'executed', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)