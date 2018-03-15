"""Buscador de videos no youtube."""
# !/usr/bin/python
# -*- coding: latin-1 -*-

import requests
import re

base_url = "https://www.youtube.com/results?page=%s&search_query="
resultados = []


class YouTube_Searcher():
    """Classe q realiza buscas no YouTube."""

    @staticmethod
    def search(titulo='', mode='s'):
        """Classe principal."""
        if titulo:
            search_query = base_url + titulo
            # print(search_query)
            req = requests.post(search_query + '&pbj=1')
            if req:
                raw_links = YouTube_Searcher.find_links(req.text)
                if raw_links:
                    links = YouTube_Searcher.format_links(raw_links)
                    if mode == 'm' or mode == 'M':
                        return links
                    else:
                        return links[0]

        return False

    @staticmethod
    def format_links(raw_links):
        """Formata os links."""
        links = []
        for raw_link in raw_links:
            links.append('https://www.youtube.com/' + raw_link)
        return links

    @staticmethod
    def find_links(page_text):
        """Dado o texto, encontra e retorna link de videos."""
        resultados = (re.findall(
            pattern='/watch?' + r'[^"]*', string=page_text))
        if len(resultados) > 0:
            return resultados
        else:
            return False
