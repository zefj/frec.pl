# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render, get_object_or_404
from django.shortcuts import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from mainsite.models import Post, About, CV, Tag, Project

from django_simple_search2 import search_handler

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

    if request.GET.get('filter'):
        filter_tag = request.GET.get('filter')
        paginated_posts = paginator(Post.objects.filter(tags__name=filter_tag).exclude(pub_date__isnull=True).order_by('-pub_date'), request.GET.get('page'))
    else:
        filter_tag = None
        paginated_posts = paginator(Post.objects.exclude(pub_date__isnull=True).order_by('-pub_date', '-id'), request.GET.get('page'))

    available_tags = [tag.name for tag in Tag.objects.all()]

    context_dict = {'posts': paginated_posts, 'filter_tag': filter_tag, 'available_tags': available_tags}

    return render(request, template_name, context_dict)

def post(request, template_name='mainsite/post.html', post_name_slug=None):
    
    requested_post = get_object_or_404(Post, slug=post_name_slug)
    context_dict = {'post': requested_post}

    return render(request, template_name, context_dict)

def about(request, template_name='mainsite/about.html'):

    about_text = About.objects.all()
    
    cv_pl = CV.objects.get_object_or_none(language='PL')
    cv_en = CV.objects.get_object_or_none(language='EN')
    
    context_dict = {'about_text': about_text, 'cv_pl': cv_pl, 'cv_en': cv_en}

    return render(request, template_name, context_dict)

def projects(request, template_name='mainsite/projects.html'):

    context_dict = {'projects': Project.objects.all()}
    
    return render(request, template_name, context_dict)

def search(request, template_name='mainsite/search_results.html'):

    model_fields = {
        'Post': ['title', 'text', 'tags__name'],
        'Tag': ['name']
    }

    query_string = request.GET['q']
    queries = search_handler(query_string, model_fields)
    
    if queries:
        found_post_entries = Post.objects.filter(queries['Post']).distinct()
        found_tags_entries = Tag.objects.filter(queries['Tag']).distinct()
        paginated_found_post_entries = paginator(found_post_entries, request.GET.get('page'))

    else:
        paginated_found_post_entries = None
        found_tags_entries = None

    return render_to_response(template_name,
                              {'query_string': query_string,
                              'search_post_results': paginated_found_post_entries,
                              'search_tag_results': found_tags_entries,
                              },
                              context_instance=RequestContext(request))

