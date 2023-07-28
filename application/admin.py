from django.contrib import admin
from application.models import Category, Brand, Device, Product
from application.models import Order, OrderProduct


admin.site.register(Brand)
admin.site.register(Device)
admin.site.register(Product)
admin.site.register(OrderProduct)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'data', 'name', ]
admin.site.register(Category, CategoryAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notes', 'submitted', 'processed', 'total']
admin.site.register(Order, OrderAdmin)