# -*- coding: utf-8 -*-
from blendy.models import ApiUsers, DailyBill
from django.db.models import F
import requests
import xml.etree.ElementTree as ET
from django.core.urlresolvers import Resolver404

import enchant
d = enchant.Dict("pl_PL") #aspell-pl z http://packages.ubuntu.com/precise/aspell-dictionary
import re
from hashlib import sha1
import hmac

import datetime

class DoesNotCompute(Exception):
    """ Easy to understand naming conventions work best! """
    pass

"""
Dzieli zdanie po spacjach, zwraca liste slow.
"""
def parser(text):

	if len(text) > 0:
		return list(set(text.split(" ")))
	else:
		return list()

"""
Przetwarza tekst za pomoca wyrazen regularnych. 

1. Usuwa znaki specjalne
2. Usuwa whitespace przed, po, oraz znaki powtorzone (np. dwie spacje)
"""
def sanitizer(text):

	text = text.encode('utf-8')
	text = re.sub('[^a-zżźćńółęąśŻŹĆĄŚĘŁÓŃA-Z0-9 ]', ' ', text) # usuwa znaki specjalne
	text = re.sub('^\s+|\s+$|\s+(?=\s)', '', text) # whitespace przed, wiecej niz 1 bez uwzglednienia jednego (np. zachowuje jedna spacje)

	return text	

def java(wordList):

	suggDict = {}
	for word in wordList:
		try:
			r = requests.get('http://localhost:8081', params = {'text': word, 'language':'pl-PL'})
			root = ET.fromstring(r.content)
			for error in root.findall('error'):
				if error.get('locqualityissuetype') == 'misspelling':
					misspell = error.get('context')
					suggestions = error.get('replacements').split('#')
					suggDict[misspell] = [x for x in suggestions]
		except:
			raise Resolver404


	return suggDict


"""
Glowna funkcja sprawdzania poprawnosci zdan. Przyjmuje liste slow, zwraca slownik z sugestiami w postaci:
	{
	'slowo': 
		['sugestia1', 'sugestia2', 'sugestia3'],
	'slowo2': 
		['sugestia1', 'sugestia2']
	}
"""
def pyenchant(wordList):
	
	suggDict = {}
	# print wordList
	
	for word in wordList:
		if not d.check(word):
			suggestions = d.suggest(word)
			suggDict[word] = [x for x in suggestions]

	return suggDict

"""
Glowny interfejs komunikacji z modulem sprawdzania poprawnosci ort., obsluga powinna odbywac sie przez ta funkcje. 
Przyjmuje nazwe silnika oraz liste slow.
"""
def spellcheckHandler(engine, wordList):

	if engine == 'java':
		return java(wordList)

	elif engine == 'enchant':
		return pyenchant(wordList)

	else:
		return False

"""
Funkcja zapisujaca ilosc sprawdzonych przez uzytkownika slow. Przyjmuje nazwe uzytkownika oraz ilosc slow. 
Ilosc slow powinna byc obliczana przez program! Np. funkcja wbudowana len() na liscie slow z funkcji utils.parser().
"""
def logger(user, words_quantity):

	billobject = DailyBill.objects.filter(user__name=user).filter(date=datetime.date.today())
	if billobject.exists():
		billobject.update(words_checked=F('words_checked')+words_quantity)
	else:
	 	billobject = DailyBill(user=ApiUsers.objects.get(name=user), words_checked = words_quantity)
	 	billobject.save()

	return

"""
Funkcja uwierzytelniajaca. Przyjmuje url zapytania, nazwe uzytkownika, dostarczony klucz API oraz sygnature zapytania.

Proces podpisywania zapytania wyglada nastepujaco:

1. URL zapytania wraz ze wszystkimi parametrami nalezy pozbawic dopisku okreslajacego nazwe aplikacji oraz poczatkowego ukosnika, przykladowa forma:
	check/?text=Rzo%C5%82nie%C5%BCe+nie+lubiom+siedzie%C4%87+w+koszarah&engine=enchant&user=mariusz&key=TVSUZIANFTYKYDM

	Nalezy pamietac o prawidlowym kodowaniu! Kodowanie znakow specjalnych UTF-8, adres po standardowym zakodowaniu znakow do ASCII, wraz z kodowaniem
	znaku " ' " (%27).

2. Ten adres nalezy zaszyfrowac algorytmem HMAC-SHA1, uzywajac do tego wygenerowanego klucza prywatnego uzytkownika ('secret').
3. Sygnature nalezy umiescic w naglowku HTTP 'Authorization'.

Serwer wykonuje powyzszy proces w ten sam sposob, obliczone sygnatury musza sie zgadzac.
"""
def authenticate_request(url, user, apikey_supplied, signature):
	try:
		userobject = ApiUsers.objects.get(name=user)
		apikey = userobject.APIKey
		secret = userobject.secret

		if apikey == apikey_supplied:
			hash = hmac.new(str(secret), str(url.decode('utf-8')), sha1)
			# print url, hash.hexdigest()
			if hash.hexdigest() != signature:
				return False

			else:
				return True

		else:
			return False	

	except ApiUsers.DoesNotExist:
		return False