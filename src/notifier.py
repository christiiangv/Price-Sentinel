import os
import requests
from src.analyzer import PriceAnalysis


class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    @property
    def is_configured(self) -> bool:
        return bool(self.token and self.chat_id)

    def send_alert(self, product_name: str, url: str, analysis: PriceAnalysis) -> bool:
        if not self.is_configured:
            return False

        badge = "🔥 MÍNIMO HISTÓRICO" if analysis.is_all_time_low else "🎯 PRECIO OBJETIVO ALCANZADO"
        message = (
            f"*{badge}*\n\n"
            f"📦 *Producto:* {product_name}\n"
            f"💰 *Precio actual:* {analysis.current_price:.2f} €\n"
            f"📉 *Mínimo registrado:* {analysis.min_price:.2f} €\n"
            f"📊 *Media histórica:* {analysis.avg_price:.2f} € (-{analysis.discount_vs_avg}%)\n\n"
            f"🔗 [Ver producto]({url})"
        )

        endpoint = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }

        try:
            res = requests.post(endpoint, json=payload, timeout=8)
            return res.status_code == 200
        except requests.RequestException:
            return False
