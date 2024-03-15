# coding=utf-8
import abc
import os
from typing import Final

from libretranslatepy import LibreTranslateAPI

LT_ENDPOINT: Final[str | None] = os.environ.get("LT_ENDPOINT", None)
LT_API_KEY: Final[str | None] = os.environ.get("LT_API_KEY", None)
LT_LANGUAGES: Final[set[str]] = {
    "ar",
    "az",
    "bg",
    "bn",
    "ca",
    "cs",
    "da",
    "de",
    "el",
    "en",
    "eo",
    "es",
    "et",
    "fa",
    "fi",
    "fr",
    "ga",
    "he",
    "hi",
    "hu",
    "id",
    "it",
    "ja",
    "ko",
    "lt",
    "lv",
    "ms",
    "nb",
    "nl",
    "pl",
    "pt",
    "ro",
    "ru",
    "sk",
    "sl",
    "sq",
    "sr",
    "sv",
    "th",
    "tl",
    "tr",
    "uk",
    "ur",
    "vi",
    "zh",
    "zt",
}


class RoundTripTranslator(abc.ABC):
    """Round-Trip-Translation (RTT) base class."""

    def __init__(self, source_lang: str, target_lang: str, *args, **kwargs):
        """RoundTripTranslator constructor.

        Args:
            source_lang (str): The source language.
            target_lang (str): The target language.
        """
        self.source_lang = source_lang
        self.target_lang = target_lang

    @abc.abstractmethod
    def rtt(self, text: str) -> str:
        """Run the round-trip-translation (RTT) on the given text.
        You should implement this method in your subclass.

        Args:
            text (str): The input text.

        Returns:
            str: The round-trip-translated text.
        """
        ...


class LibreTranslateRTT(RoundTripTranslator):

    def __init__(
        self,
        target_lang: str,
        source_lang: str = "en",
        url: str = LT_ENDPOINT,
        api_key: str | None = LT_API_KEY,
    ):
        """LibreTranslate RTT implementation.

        Note:
            LibreTranslate will only translate between english and another supported language.

        Args:
            target_lang (str): The target language.
            source_lang (str, optional): The source language. Defaults to `"en"`.
            url (str): The LibreTranslate API endpoint.
                Can be set via and defaults to environment variable `LT_ENDPOINT`.
            api_key (str, optional): The LibreTranslate API key.
                Can be set via and defaults to environment variable `LT_API_KEY`.
        """
        if url is None:
            raise ValueError(
                "url must be given. Either set LT_ENDPOINT environment variable or pass a valid url."
            )

        # fmt: off
        if (invalid := source_lang) not in LT_LANGUAGES or (invalid := target_lang) not in LT_LANGUAGES:
            raise ValueError(
                f"Invalid language '{invalid}', must be one of {LT_LANGUAGES}"
            )
        # fmt: on

        super().__init__(source_lang, target_lang)
        self.lt = LibreTranslateAPI(url, api_key=api_key)

    def rtt(self, text: str) -> str:
        text_t = self.lt.translate(text, self.source_lang, self.target_lang)
        return self.lt.translate(text_t, self.target_lang, self.source_lang)


if __name__ == "__main__":
    # example usage with libretranslate/libretranslate docker image
    rtt = LibreTranslateRTT("fr", url="http://localhost:5000")
    print(rtt.rtt("Hello, world!"))  # Hello, people!
