from django.contrib import admin
from django.contrib.admin import display
from .models import *

admin.site.register(Gender)
admin.site.register(ColorProduct)
admin.site.register(SizeProduct)
admin.site.register(CollectionProduct)
admin.site.register(UpperMaterialProduct)
admin.site.register(LiningMaterialProduct)
admin.site.register(OutsoleMaterialProduct)
admin.site.register(InsoleMaterialProduct)
admin.site.register(CountryOfManufacture)
admin.site.register(BrandOfManufacture)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    prepopulated_fields = {'url': ('name',)}

admin.site.register(Category, CategoryAdmin)


class ShoeAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'price', 'discount', 'discounted_price_column', 'stock', 'available']
    list_filter = ['available', 'country_of_manufacture', 'size', 'color', 'collection', 'gender', 'brand']
    list_editable = ['price', 'discount', 'stock', 'available']
    readonly_fields = ('discounted_price',)
    search_fields = ('name',)
    actions = ['publish', 'unpublish']
    prepopulated_fields = {'url': ('name',)}

    @display(description='Цена со скидкой')
    def discounted_price_column(self, obj):
        return obj.discounted_price

    def unpublish(self, request, queryset):
        row_update = queryset.update(available=True)
        if row_update == 1:
            message_bit = "Запись была обновлена"
        else:
            message_bit = f"{row_update} записей было обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(available=False)
        if row_update == 1:
            message_bit = "Запись была обновлена"
        else:
            message_bit = f"{row_update} записей было обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Товар закончился"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Товар появился в продаже"
    unpublish.allowed_permissions = ('change',)


admin.site.register(Shoes, ShoeAdmin)
admin.site.register(RatingStar)
admin.site.register(Review)
admin.site.register(Comment)


class RatingStarAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        # Автоматическое создание 5 звёзд
        if RatingStar.objects.count() == 0:
            for i in range(1, 6):
                RatingStar.objects.create(value=i)
        return super().get_actions(request)