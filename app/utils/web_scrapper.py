import requests
from bs4 import BeautifulSoup
import re
import html
import unicodedata


class WebScrapper:
    def __init__(self, urls: list[str]) -> None:
        self.urls = urls

    @staticmethod
    def scrape_single_url(url: str):
        r = requests.get(url, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")
        # remove scripts, styles and obvious boilerplate containers
        for tag in soup(
            ["script", "style", "noscript", "header", "footer", "nav", "aside"]
        ):
            tag.decompose()
        # prefer article/main content when available
        main = soup.find("main") or soup.find("article")
        if main:
            parts = [
                p.get_text(separator=" ", strip=True)
                for p in main.find_all(["p", "h1", "h2", "h3", "li"])
            ]
        else:
            parts = [p.get_text(separator=" ", strip=True) for p in soup.find_all("p")]
        text = " ".join(parts)

        return text

    @staticmethod
    def clean_data(text: str):
        if not text:
            return ""
        # HTML entities -> chars
        text = html.unescape(text)
        # normalize unicode
        text = unicodedata.normalize("NFKC", text)
        # remove common reference markers like [1]
        text = re.sub(r"\[\d+\]", "", text)
        # remove urls and emails
        text = re.sub(r"http[s]?://\S+", "", text)
        text = re.sub(r"\S+@\S+", "", text)
        # collapse whitespace
        text = re.sub(r"\s+", " ", text).strip()
        # remove very long repeated characters
        text = re.sub(r"(.)\1{4,}", r"\1", text)
        # drop non-printable
        text = "".join(ch for ch in text if ch.isprintable())
        # discard very short scraps
        if len(text) < 50:
            return ""
        return text

    def scrape_all_urls(self):
        all_data = []
        for url in self.urls:
            site_data = self.scrape_single_url(url=url)
            clean_data = self.clean_data(site_data)
            all_data.append(clean_data)

        return all_data


if __name__ == "__main__":
    urls = [
        "https://www.tatamotors.com/careers/faqs",
        "https://www.tatamotors.com/corporate-responsibility/planet-resilience/",
    ]

    webScrapper = WebScrapper(urls)
    all_data = webScrapper.scrape_all_urls()
    print(all_data)
