#!/usr/bin/python
# Python wordnik vocab list generator

import sys
import urllib2
import json

def getWord(word):
	word = word
	api_key = '353429f36471b45d4f9000d878d09afe954cfdb645cd306cf'

	url = 'http://api.wordnik.com//v4/word.json/' + word + '/definitions?includeRelated=false&includeTags=false&limit=3&useCanonical=true&api_key=' + api_key

	jsondata = urllib2.urlopen(url)

	j = json.load(jsondata)

	pos = j[0]['partOfSpeech']
	definition =  j[0]['text']
	nicelist = [word, pos, definition]
	return nicelist

done = 'n'
num = 1
prompt = '> '
wordlist = []

while done == 'n':
	print 'Word #' + str(num)
	print 'Type done when finished.'
	word = raw_input(prompt)
	if word == 'done':
		break
	else:
		wordlist.append(word)
		num = num+1

print 'Words to define:'

for words in wordlist:
	print words

for word in wordlist:
	nicelist = getWord(word)
	thingtowrite = nicelist[0] + ' | ' + nicelist[1] + ' | ' + nicelist[2] + '\n'
	thingtowrite = thingtowrite.encode('ascii', 'ignore')
	print thingtowrite
	f = open('definitions.txt', 'a')
	f.write(thingtowrite)
	f.close
