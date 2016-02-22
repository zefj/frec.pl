# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from blendy.models import ApiUsers, DailyBill
from django.http import HttpResponseForbidden, HttpResponseBadRequest

from blendy import utils

def home(request, template_name='blendy/home.html'):

    context_dict = {}
    return render(request, template_name, context_dict)

def checkSpelling(request):

	if request.method == 'GET':

		if not request.GET.get('user') or not request.GET.get('key') or not request.GET.get('engine') in ['enchant', 'java']:
			return HttpResponseBadRequest()

		user = request.GET.get('user')
		apikey_supplied = request.GET.get('key')
		url = 'check/?'+request.META['QUERY_STRING'].decode('utf-8') # hack...
		signature = request.META['HTTP_AUTHORIZATION']
		auth = utils.authorize(url, user, apikey_supplied, signature)

		if auth:
			query = request.GET.get('text')

			escapedQuery = utils.sanitizer(query)
			wordList = utils.parser(escapedQuery)
			engine = request.GET.get('engine')			
			replacements = utils.spellcheckHandler(engine, wordList)			

			response_data = {}
			response_data['query'] = query
			response_data['escapedquery'] = escapedQuery
			response_data['words'] = wordList
			response_data['replacements'] = replacements

			utils.logger(user, len(wordList))

			return JsonResponse(response_data)

		else:
			return HttpResponseForbidden()