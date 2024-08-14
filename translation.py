#!/usr/bin/env python
# coding: utf-8

import os
from configparser import ConfigParser


class Language:

    def __init__(self, langCode, langName, d):

        self.code = langCode
        self.name = langName
        self.dict = d

    def __getitem__(self, item):

        return self.dict[item]


class TDatabase:
    def __init__(self):
        self.languages = {}
        self.langAvailable = []

        self.load_languages()

    def load_languages(self):
        cp = ConfigParser()
        lang_dir = "lang"

        for lang_file in os.listdir(lang_dir):
            cp.read(os.path.join(lang_dir, lang_file))
            langname = cp.get("_lang", "name")

            sections = {section: dict(cp.items(section)) for section in cp.sections() if section != "_lang"}

            self.languages[lang_file] = Language(lang_file, langname, sections)
            self.langAvailable.append(lang_file)

        self.langNum = len(self.languages)

    def getText(self, lang, sect, ident):

        return self.languages[lang][sect][ident]
