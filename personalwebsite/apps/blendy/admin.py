from django.contrib import admin
from blendy.models import ApiUser, ApiUserGroup, DailyUsageLog
from django.db.models import Sum

@admin.register(ApiUser)
class ApiUserAdmin(admin.ModelAdmin):
    def group_api_key(self):
	    return self.group.APIKey

    list_display = (
        'user', 'group', 'secret', group_api_key
        )

@admin.register(ApiUserGroup)
class ApiUserGroupAdmin(admin.ModelAdmin):
    def total_checked(self):
    	q = DailyUsageLog.objects.filter(group=self).aggregate(total = Sum('words_checked'))

    	return q['total']

    list_display = (
        'group', 'APIKey', total_checked
        ) 

@admin.register(DailyUsageLog)
class DailyUsageLogAdmin(admin.ModelAdmin):
    list_display = (
        'group', 'date', 'words_checked'
        )