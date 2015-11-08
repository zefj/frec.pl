from django.contrib import admin

from mainsite.models import Tag, Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = (
		'id', 'title', 'pub_date', 'get_tags'
		)
	list_display_links = (('id', 'title', 'pub_date'))
	exclude = ('slug',)

admin.site.register(Tag)