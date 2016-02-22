from django.contrib import admin
from blendy.models import ApiUsers, DailyBill

@admin.register(ApiUsers)
class ApiUsersAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'APIKey'
        )

@admin.register(DailyBill)
class DailyBillAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'date', 'words_checked'
        ) 