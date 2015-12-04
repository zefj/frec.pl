from django.contrib import admin
from django.conf import settings
import os
from mainsite.models import Tag, Post, CV, About, Project

"""
Django.admin by default doesn't call delete() model method. This custom admin action makes sure it does.
"""
def delete_selected_with_file(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'pub_date', 'get_tags'
        )
    list_display_links = (('id', 'title', 'pub_date'))
    exclude = ('slug',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'rank'
        )


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'language', 'upload_date'
        )
    list_display_links = (('language', 'upload_date'))
    actions = [delete_selected_with_file]
    delete_selected_with_file.short_description = "Delete selected CVs"

    def get_actions(self, request):
        actions = super(CVAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(Tag)
admin.site.register(About)
