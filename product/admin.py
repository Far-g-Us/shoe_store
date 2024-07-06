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
admin.site.register(CountryOfManufacture)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    prepopulated_fields = {'url': ('name',)}

admin.site.register(Category, CategoryAdmin)


class ShoeAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'price', 'discount', 'stock', 'available']
    list_filter = ['available', 'country_of_manufacture', 'size', 'color', 'collection', 'gender', 'brand']
    list_editable = ['price', 'discount', 'stock', 'available']
    actions = ['publish', 'unpublish']
    prepopulated_fields = {'url': ('name',)}

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
admin.site.register(Rating)
admin.site.register(Review)