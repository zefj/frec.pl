# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render, get_object_or_404
from django.shortcuts import RequestContext

from mainsite.models import Post
from mainsite.utils import get_query

def blog(request, template_name='mainsite/blog.html'):

	context_dict = {'posts': Post.objects.filter(visible=True).order_by('-pub_date')}

	return render(request, template_name, context_dict)

def post(request, template_name='mainsite/post.html', post_name_slug=None):
	
	if post_name_slug:

		requested_post = get_object_or_404(Post, slug=post_name_slug)
		context_dict = {'post': requested_post}

	return render(request, template_name, context_dict)

def about(request, template_name='mainsite/about.html'):

	return render_to_response(template_name, RequestContext(request, {}))

def search(request, template_name='mainsite/search_results.html'):

	query_string = ''
	found_entries = None
	if 'q' in request.GET and request.GET['q'].strip() and request.GET['q'] != '':
	    query_string = request.GET['q']
	    
	    entry_query = get_query(query_string, ['title', 'text', 'tags__name'])

	    print entry_query

	    found_entries = Post.objects.filter(entry_query).distinct()
	    
	    print found_entries

	    return render_to_response(template_name,
	                              {'query_string': query_string,
	                                  'search_results': found_entries},
	                              context_instance=RequestContext(request))

	else:
	    return render_to_response(template_name,
	                              {'query_string': query_string},
	                              context_instance=RequestContext(request))

