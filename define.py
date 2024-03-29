#!/usr/bin/python

import sys
import os
import unicodedata
import __main__

from PyRTF import *

from wordnik.api.APIClient import APIClient
from wordnik.api.WordAPI import WordAPI

import wordnik.model

api_key = '353429f36471b45d4f9000d878d09afe954cfdb645cd306cf'
client = APIClient(api_key, 'http://api.wordnik.com/v4')

def read_file():
    global words
    words = []
    f = open(input_name, 'r')
    for line in f:
        words.append(line.split()[0].lower())
    f.close()

def get_def(word):
    wordAPI = WordAPI(client)
    input = wordnik.model.WordDefinitionsInput.WordDefinitionsInput()
    input.word = word
    input.limit = 2
    input.useCanonical = True
    input.sourceDictionaries = 'webster'
    definitions = wordAPI.getDefinitions(input)
    def_list = []
    if definitions:
        for definition in definitions:
            def_list.append(definition.text)
    return def_list

def get_pos(word):
    wordAPI = WordAPI(client)
    input = wordnik.model.WordDefinitionsInput.WordDefinitionsInput()
    input.word = word
    input.limit = 2
    input.useCanonical = True
    input.sourceDictionaries = 'webster'
    definitions = wordAPI.getDefinitions(input)
    pos_list = []
    if definitions:
        for definition in definitions:
            pos_list.append(definition.partOfSpeech)
    return pos_list

def generate_rtf():
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)

    word_style = TextPS(size=32, bold=True)
    def_style = TextPS()

    for word in words:
        p = Paragraph(Text(word, word_style))
        section.append(p)
        def_list = get_def(word)
        pos_list = get_pos(word)
        for a, b in zip(def_list, pos_list):
            if a != None and b != None:
                a = a.encode('ascii', 'ignore')
                p = Paragraph(Text('(%s) - %s' % (b, a), def_style))
                section.append(p)
    return doc

def write_file():
    DR = Renderer()
    f = open(output_name, 'w')
    DR.Write(generate_rtf(), f)
    f.close()

def main():
    read_file()
    generate_rtf()
    write_file()

if len(sys.argv) != 3:
    sys.exit('Usage: %s <input file> <output file>' % __main__.__file__)

input_name = sys.argv[1]
output_name = sys.argv[2]

if __name__ == '__main__':
    main()