# -*- coding: utf-8 -*-
from blendy.models import ApiUsers, DailyBill
from django.db.models import F

import enchant
d = enchant.Dict("pl_PL") #aspell-pl z http://packages.ubuntu.com/precise/aspell-dictionary
import re
from hashlib import sha1
import hmac

import datetime

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

def java(text):
	pass

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

	if engine == 'google':
		return google(wordList)

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
Funkcja autoryzujaca.
"""
def authorize(url, user, apikey_supplied, signature):

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