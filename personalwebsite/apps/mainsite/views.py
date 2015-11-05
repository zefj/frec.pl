# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext

def home(request):
    return render_to_response('base.html', RequestContext(request, {}))
