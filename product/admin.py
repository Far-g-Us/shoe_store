from django.contrib import admin
from .models import *


admin.site.register(ColorProduct)
admin.site.register(SizeProduct)
admin.site.register(CollectionProduct)
# admin.site.register(DiscountProduct)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    prepopulated_fields = {'url': ('name',)}
admin.site.register(Category, CategoryAdmin)

class ShoeAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'price', 'discount', 'stock', 'available']
    list_filter = ['available']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'url': ('name',)}
admin.site.register(Shoes, ShoeAdmin)

admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Review)