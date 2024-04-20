from django.contrib import admin
from .models import *


admin.site.register(ColorProduct)
admin.site.register(SizeProduct)
admin.site.register(CollectionProduct)
admin.site.register(DiscountProduct)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class ShoeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount', 'stock', 'available']
    list_filter = ['available']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Shoes, ShoeAdmin)
