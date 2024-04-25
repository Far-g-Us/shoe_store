from django.contrib import admin
from .models import *

admin.site.register(Gender)
admin.site.register(ColorProduct)
admin.site.register(SizeProduct)
admin.site.register(CollectionProduct)
admin.site.register(UpperMaterialProduct)
admin.site.register(LiningMaterialProduct)
admin.site.register(OutsoleMaterialProduct)
admin.site.register(InsoleMaterialProduct)
# admin.site.register(DiscountProduct)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    prepopulated_fields = {'url': ('name',)}
admin.site.register(Category, CategoryAdmin)

class ShoeAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'price', 'discount', 'stock', 'available', 'сountry_of_manufacture']
    list_filter = ['available', 'сountry_of_manufacture']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'url': ('name',)}
admin.site.register(Shoes, ShoeAdmin)

admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Review)