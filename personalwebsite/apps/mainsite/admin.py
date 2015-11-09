from django.contrib import admin

from mainsite.models import Tag, Post, CV

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = (
		'id', 'title', 'pub_date', 'get_tags'
		)
	list_display_links = (('id', 'title', 'pub_date'))
	exclude = ('slug',)

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
	list_display = (
		'language', 'upload_date'
		)
	list_display_links = (('language', 'upload_date'))

admin.site.register(Tag)
