from src.scraper import PriceScraper
from src.analyzer import PriceAnalyzer


def test_parse_european_price():
    assert PriceScraper.parse_price("1.249,90 €") == 1249.90
    assert PriceScraper.parse_price("49,95€") == 49.95


def test_parse_us_price():
    assert PriceScraper.parse_price("$1,299.50") == 1299.50


def test_target_price_alert():
    result = PriceAnalyzer.analyze(current_price=80.0, history=[100.0, 95.0, 90.0], target_price=85.0)
    assert result.is_target_reached is True
    assert result.is_all_time_low is True
    assert result.min_price == 80.0
