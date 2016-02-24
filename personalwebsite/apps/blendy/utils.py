# -*- coding: utf-8 -*-
from django.utils.encoding import smart_text
from django.db.models import F
from django.core.urlresolvers import Resolver404
from blendy.models import ApiUser, ApiUserGroup, DailyUsageLog

import datetime
import re
import requests
import hmac
from hashlib import sha1
import xml.etree.ElementTree as ET

import enchant
d = enchant.Dict("pl_PL") #aspell-pl z http://packages.ubuntu.com/precise/aspell-dictionary

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

1. Usuwa znaki specjalne z wylaczeniem polskich
2. Usuwa whitespace przed, po, oraz znaki powtorzone (np. dwie spacje)
"""
def sanitizer(text):

    text = smart_text(text, encoding='utf-8', strings_only=False, errors='strict')
    regex = smart_text('[^a-zżźćńółęąśŻŹĆĄŚĘŁÓŃA-Z0-9]', encoding='utf-8', strings_only=False, errors='strict')
    text = re.sub(regex, ' ', text) # usuwa znaki specjalne
    text = re.sub('^\s+|\s+$|\s+(?=\s)', '', text) # whitespace przed, wiecej niz 1 bez uwzglednienia jednego (np. zachowuje jedna spacje)
 
    return text 

"""
Funkcja sprawdzania poprawnosci zdan za pomoca serwera programu languagetool (languagetool.org). Przyjmuje liste slow, zwraca slownik z sugestiami w postaci:
    {
    'slowo': 
        ['sugestia1', 'sugestia2', 'sugestia3'],
    'slowo2': 
        ['sugestia1', 'sugestia2']
    }

Serwer musi zostac wczesniej uruchomiony i nasluchiwac na porcie 8081.
"""
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
Funkcja sprawdzania poprawnosci zdan za pomoca biblioteki enchant. Przyjmuje liste slow, zwraca slownik z sugestiami w postaci:
    {
    'slowo': 
        ['sugestia1', 'sugestia2', 'sugestia3'],
    'slowo2': 
        ['sugestia1', 'sugestia2']
    }
"""
def pyenchant(wordList):
    
    suggDict = {}
    
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
    print wordList
    
    if engine == 'java':
        return java(wordList)

    elif engine == 'enchant':
        return pyenchant(wordList)

    else:
        return False

"""
Funkcja zapisujaca ilosc sprawdzonych przez uzytkownika slow. Przyjmuje nazwe uzytkownika oraz ilosc slow. Ilosc ta naliczana jest na konto grupy 
uzytkownikow API, do ktorej nalezy uzytkownik. 
"""
def logger(username, words_quantity):

    user = ApiUser.objects.get(user__username=username)

    daily_group_log_object = DailyUsageLog.objects.filter(group=user.group).filter(date=datetime.date.today())
    if daily_group_log_object.exists():
        daily_group_log_object.update(words_checked=F('words_checked')+words_quantity)
    else:
        daily_group_log_object = DailyUsageLog(group=user.group, words_checked = words_quantity)
        daily_group_log_object.save()
    return

"""
Funkcja uwierzytelniajaca zapytania z zewnatrz. Przyjmuje url zapytania, nazwe uzytkownika, dostarczony klucz API oraz sygnature zapytania.

Proces podpisywania zapytania wyglada nastepujaco:

1. URL zapytania wraz ze wszystkimi parametrami nalezy pozbawic dopisku okreslajacego nazwe aplikacji oraz poczatkowego ukosnika, przykladowa forma:
    check/?text=Rzo%C5%82nie%C5%BCe+nie+lubiom+siedzie%C4%87+w+koszarah&engine=enchant&user=mariusz&key=TVSUZIANFTYKYDM

    Nalezy pamietac o prawidlowym kodowaniu! Kodowanie znakow specjalnych UTF-8, adres po standardowym zakodowaniu znakow do ASCII, wraz z kodowaniem
    znaku " ' " (%27).

2. Ten adres nalezy zaszyfrowac algorytmem HMAC-SHA1, uzywajac do tego wygenerowanego klucza prywatnego uzytkownika ('secret').
3. Sygnature nalezy umiescic w naglowku HTTP 'Authorization'.

Serwer wykonuje powyzszy proces w ten sam sposob, obliczone sygnatury musza sie zgadzac.
"""
def authenticate_external_request(url, username, apikey_supplied, signature):
    try:
        userobject = ApiUser.objects.get(user__username=username)
        apikey = userobject.group.APIKey
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

    except ApiUser.DoesNotExist:
        return False

"""
Funkcja uwierzytelniajaca zapytania wewnetrzne (z uzyciem systemu uzytkownikow). Przyjmuje objekt uzytkownika.
"""
def authenticate_internal_request(user):
    try:
        userobject = ApiUser.objects.get(user=user) 

        if user:
            return True
        else:
            return False

    except ApiUser.DoesNotExist:
        return False    