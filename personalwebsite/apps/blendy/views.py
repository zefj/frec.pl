# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from blendy import utils
from functools import wraps

def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper
   
def user_login(request, template_name='blendy/login.html'):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('blendy:home'))

        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Wprowadzono błędne dane.")
    else:
        return render(request, template_name, {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('blendy:home'))

@login_required
def home(request, template_name='blendy/home.html'):
    context_dict = {}
    return render(request, template_name, context_dict)

"""
Widok uslugi sprawdzania poprawnosci ortograficznej dla zastosowan zewnetrznych. Widok odpowiada na zapytania metodami GET.

Wymagane parametry:
	text - tekst do sprawdzenia poprawnosci ortograficznej,
	user - nazwa uzytkownika,
	key - przydzielony klucz api,
	engine - silnik {enchant, java},

Oraz dodatkowo sygnatura zapytania w parametrze HTTP 'Authorization'.

Sygnatura tworzona jest z polaczenia adresu url (bez pierwszej sciezki) oraz sekretu. Opis procesu znajduje sie
w dokumentacji, oraz w pliku utils.py przy metodzie authenticate_request().

Przykladowy URL dla zdania "Rzołnieże nie lubiom siedzieć w koszarah": 

check/?text=Rzo%C5%82nie%C5%BCe+nie+lubiom+siedzie%C4%87+w+koszarah&engine=enchant&user=mariusz&key=TVSUZIANFTYKYDM

Widok zwraca odpowiedz w formacie JSON, blad 403 (Forbidden) lub 400 (Bad Request), w przypadku sukcesu zawiera:
	query - przeslany tekst do sprawdzenia,
	escapedquery - tekst przetworzony funkcja sanitizer() z modulu utils
	words - lista zidentyfikowanych slow
	replacements - sugestie zmian do ww. slow
"""
def checkSpelling(request):

	if request.method == 'GET':
		if (not request.GET.get('user') 
				or not request.GET.get('key') 
				or not request.GET.get('engine') in ['enchant', 'java'] 
				or not 'HTTP_AUTHORIZATION' in request.META):

			return HttpResponseBadRequest()

		user = request.GET.get('user')
		apikey_supplied = request.GET.get('key')
		url = 'check/?'+request.META['QUERY_STRING'].decode('utf-8') # hack...
		signature = request.META['HTTP_AUTHORIZATION']
		auth = utils.authenticate_request(url, user, apikey_supplied, signature)

		if auth:

			query = request.GET.get('text')
			escapedQuery = utils.sanitizer(query)
			wordList = utils.parser(escapedQuery)
			engine = request.GET.get('engine')			
			replacements = utils.spellcheckHandler(engine, escapedQuery, wordList)			

			response_data = {}
			response_data['query'] = query
			response_data['escapedquery'] = escapedQuery
			response_data['words'] = wordList
			response_data['replacements'] = replacements

			utils.logger(user, len(wordList))

			return JsonResponse(response_data)

		else:
			return HttpResponseForbidden()

"""
Widok uslugi sprawdzania poprawnosci ortograficznej dla zastosowan wewnetrznych. Widok odpowiada na zapytania metodami GET.

Z uslugi korzystac moga tylko uzytkownicy zalogowani w systemie.

Wymagane parametry:
	text - tekst do sprawdzenia poprawnosci ortograficznej,
	engine - silnik {enchant, java},

Przykladowy URL dla zdania "Rzołnieże nie lubiom siedzieć w koszarah": 

check_int/?text=Rzo%C5%82nie%C5%BCe+nie+lubiom+siedzie%C4%87+w+koszarah&engine=enchant&user=mariusz&key=TVSUZIANFTYKYDM

Widok zwraca odpowiedz w formacie JSON, blad 403 (Forbidden) lub 400 (Bad Request), w przypadku sukcesu zawiera:
	query - przeslany tekst do sprawdzenia,
	escapedquery - tekst przetworzony funkcja sanitizer() z modulu utils
	words - lista zidentyfikowanych slow
	replacements - sugestie zmian do ww. slow
"""
@ajax_login_required
def checkSpelling_int(request):

	if request.method == 'GET':
		if not request.GET.get('engine') in ['enchant', 'java']:
			return HttpResponseBadRequest()

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

		return JsonResponse(response_data)

	else:
		return HttpResponseForbidden()