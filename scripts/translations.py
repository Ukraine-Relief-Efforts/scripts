#!/usr/bin/env python

from copy import copy
from typing import Final

import pandas
import requests

SCRAPER_URL: Final[
    str
] = "https://g11d3ghry9.execute-api.us-east-1.amazonaws.com/v1/country?country="
SUPPORTED_COUNTRIES: Final[list[str]] = [
    "poland-pl",
    "hungary-hu",
    "romania-ro",
    "moldova-ro",
]
SUPPORTED_LANGUAGES: Final[list[str]] = [
    "de",
    "en",
    "es",
    "it",
    "kr",
    "pl",
    "rs",
    "ua",
    "hu",
    "ro",
    "ru",
]
SOURCE_COMBINATIONS: Final[list[tuple[str, str]]] = [
    ("poland", "pl"),
    ("hungary", "hu"),
    ("romania", "ro"),
    ("moldova", "ro"),
]


def _get_sentences(country_key: str) -> list[str]:
    response: dict = requests.get(url=SCRAPER_URL + country_key).json()
    return response["general"]


if __name__ == "__main__":
    output = {}
    for country, language_ in SOURCE_COMBINATIONS:
        languages: list[str] = copy(SUPPORTED_LANGUAGES)
        languages.remove(language_)
        languages.insert(0, language_)

        sentences: list[list[str]] = []
        for language in languages:
            sentences.append(_get_sentences(f"{country}-{language}"))

        output[country] = {
            lang: sentences[index] for index, lang in enumerate(languages)
        }

    with pandas.ExcelWriter("translations.xlsx") as writer:
        for country, _ in SOURCE_COMBINATIONS:
            pandas.DataFrame.from_dict(output[country]).to_excel(
                writer, sheet_name=country
            )
