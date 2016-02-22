# -*- coding: utf-8 -*-
from blendy.models import ApiUsers, DailyBill
from django.db.models import F

import enchant
d = enchant.Dict("pl_PL") #aspell-pl z http://packages.ubuntu.com/precise/aspell-dictionary
import re
from hashlib import sha1
import hmac

import datetime

def parser(text):

	if len(text) > 0:
		return list(set(text.split(" ")))
	else:
		return list()

def sanitizer(text):

	text = text.encode('utf-8')
	text = re.sub('[^a-zżźćńółęąśŻŹĆĄŚĘŁÓŃA-Z0-9 ]', ' ', text) # usuwa znaki specjalne
	text = re.sub('^\s+|\s+$|\s+(?=\s)', '', text) # whitespace przed, wiecej niz 1 bez uwzglednienia jednego (np. zachowuje jedna spacje)

	return text	

def java(text):
	pass

def pyenchant(wordList):
	
	suggDict = {}
	# print wordList
	
	for word in wordList:
		if not d.check(word):
			suggestions = d.suggest(word)
			suggDict[word] = [x for x in suggestions]

	return suggDict

def spellcheckHandler(engine, wordList):

	if engine == 'google':
		return google(wordList)

	elif engine == 'enchant':
		return pyenchant(wordList)

	else:
		return False

def logger(user, words_quantity):

	billobject = DailyBill.objects.filter(user__name=user).filter(date=datetime.date.today())
	if billobject.exists():
		billobject.update(words_checked=F('words_checked')+words_quantity)
	else:
	 	billobject = DailyBill(user=ApiUsers.objects.get(name=user), words_checked = words_quantity)
	 	billobject.save()

	return

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