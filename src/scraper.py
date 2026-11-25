import re
import requests
from bs4 import BeautifulSoup
from typing import Optional


class PriceScraper:
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    }

    @staticmethod
    def parse_price(raw_text: str) -> Optional[float]:
        """Convierte cadenas como '1.299,95 €' o '$49.99' en float."""
        cleaned = re.sub(r"[^\d.,]", "", raw_text).strip()
        if not cleaned:
            return None

        if "," in cleaned and "." in cleaned:
            if cleaned.rfind(",") > cleaned.rfind("."):
                cleaned = cleaned.replace(".", "").replace(",", ".")
            else:
                cleaned = cleaned.replace(",", "")
        elif "," in cleaned:
            cleaned = cleaned.replace(",", ".")

        try:
            return round(float(cleaned), 2)
        except ValueError:
            return None

    def fetch_price(self, url: str, css_selector: str, timeout: int = 10) -> Optional[float]:
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            element = soup.select_one(css_selector)

            if not element:
                return None

            return self.parse_price(element.get_text())
        except requests.RequestException:
            return None
