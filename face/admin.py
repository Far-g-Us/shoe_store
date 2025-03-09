from django.contrib import admin
from django.contrib.admin import display
from .models import *

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'available')
    list_filter = ('available',)
    search_fields = ('title', 'product__name')

@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "product", "price", "discount", "discounted_price", "available")
    list_filter = ('available',)
    readonly_fields = ("discounted_price",)
    search_fields = ('title', 'product__name')
    list_editable = ('price', 'discount', 'available')
    ordering = ('-available', 'title')

    @display(description="Цена со скидкой")
    def discounted_price_column(self, obj):
        return obj.discounted_price