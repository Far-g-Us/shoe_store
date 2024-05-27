from django.contrib import admin
from reguser.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'birthday', 'email', 'created_at')
    search_fields = ('username', 'full_name')
