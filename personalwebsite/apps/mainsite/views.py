# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render, get_object_or_404
from django.shortcuts import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from mainsite.models import Post, About, CV
from mainsite.utils import get_query

def paginator(model_objects, page_number):

    posts_per_page = getattr(settings, "ELEMENTS_PER_PAGE")

    paginator_function = Paginator(model_objects, posts_per_page)

    try:
        objects = paginator_function.page(page_number)
    except PageNotAnInteger:
        objects = paginator_function.page(1)
    except EmptyPage:
        objects = paginator_function.page(paginator_function.num_pages)

    return objects

def blog(request, template_name='mainsite/blog.html'):

    paginated_posts = paginator(Post.objects.exclude(pub_date__isnull=True).order_by('-pub_date'), request.GET.get('page'))

    context_dict = {'posts': paginated_posts}

    return render(request, template_name, context_dict)

def post(request, template_name='mainsite/post.html', post_name_slug=None):
    
    if post_name_slug:

        requested_post = get_object_or_404(Post, slug=post_name_slug)
        context_dict = {'post': requested_post}

    return render(request, template_name, context_dict)

def about(request, template_name='mainsite/about.html'):

    about_text = About.objects.all()
    
    cv_pl = CV.objects.get_object_or_none(language='PL')
    cv_en = CV.objects.get_object_or_none(language='EN')
    
    context_dict = {'about_text': about_text, 'cv_pl': cv_pl, 'cv_en': cv_en}

    return render(request, template_name, context_dict)

def search(request, template_name='mainsite/search_results.html'):

    """ TODO:

    wyswietlanie wynikow wyszukiwania w tagach i postach osobno

    """

    query_string = ''
    found_entries = None
    if 'q' in request.GET and request.GET['q'].strip() and request.GET['q'] != '':
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['title', 'text', 'tags__name'])

        

        found_entries = Post.objects.filter(entry_query).distinct()
        
        paginated_found_entries = paginator(found_entries, request.GET.get('page'))

        return render_to_response(template_name,
                                  {'query_string': query_string,
                                      'search_results': paginated_found_entries},
                                  context_instance=RequestContext(request))

    else:
        return render_to_response(template_name,
                                  {'query_string': query_string},
                                  context_instance=RequestContext(request))
