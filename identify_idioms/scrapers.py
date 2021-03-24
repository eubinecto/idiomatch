from typing import List, Optional
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup, Tag


# experimenting with functional programming in python
class Failure:
    """
    code reference: https://medium.com/swlh/monads-in-python-e3c9592285d6
    the only difference is that I'm overriding rshift, not or.
    """
    def __init__(self, data, failed: bool = False, failed_msg: str = None):
        self.data = data
        self.failed = failed
        self.failed_msg = failed_msg

    def __str__(self):
        return " ".join([str(self.data), str(self.failed)])

    def __rshift__(self, f):  # >>
        return self.bind(f)

    def bind(self, f):
        if self.failed:
            return self
        try:
            x = f(self.data)
            return Failure(x)
        # handle exceptions here.... perhaps?
        except Exception as e:
            # why would this help?
            # because you don't want a big, big job to fail in the middle of the night.
            # you may want to be absolutely sure that the job won't fail at least, albeit
            # the results might be None. Better have something than nothing.
            return Failure(None, failed=True, failed_msg=str(e))


class AltsScraper:
    """
    alternatives builder. scrapes the alternatives of the given lemma from
    wiktionary. Built with monad design pattern.
    """
    WIKTIONARY_ENDPOINT = "https://en.wiktionary.org/wiki/{lemma}"
    ALTS_SPAN_ID = "Alternative_forms"

    def fetch(self, idiom: str) -> List[str]:
        # the order must be kept.
        alts: Optional[List[str]] = (
            Failure(idiom)
            >> self.build_url
            >> self.scrape_html
            >> self.build_soup
            >> self.find_alts_span
            >> self.find_alts_h3
            >> self.find_alts_ul
            >> self.find_alts_anchors
            >> self.build_alts
        ).data
        if isinstance(alts, list):
            return alts
        return list()  # this should be the default.

    @classmethod
    def build_url(cls, idiom: str) -> str:
        idiom_encoded = quote_plus(idiom.replace(" ", "_"))
        return cls.WIKTIONARY_ENDPOINT.format(lemma=idiom_encoded)

    @classmethod
    def scrape_html(cls, url: str) -> str:
        r = requests.get(url)
        r.raise_for_status()
        return r.text

    @classmethod
    def build_soup(cls, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')

    @classmethod
    def find_alts_span(cls, soup: BeautifulSoup) -> Tag:
        return soup.find('span', attrs={'id': cls.ALTS_SPAN_ID})

    @classmethod
    def find_alts_h3(cls, alts_span: Tag) -> Tag:
        return alts_span.parent

    @classmethod
    def find_alts_ul(cls, alts_h3: Tag) -> Tag:
        return alts_h3.next_sibling.next_sibling

    @classmethod
    def find_alts_anchors(cls, alts_ul: Tag) -> List[Tag]:
        return [
            anchor
            for anchor in alts_ul.find_all('a')
            if anchor.get('title', None)   # attribute title must exist e.g. don't want [1]
        ]

    @classmethod
    def build_alts(cls, alts_anchors: List[Tag]) -> List[str]:
        return [
            alt_a.text.strip()
            for alt_a in alts_anchors
        ]
