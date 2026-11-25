from dataclasses import dataclass
from typing import List


@dataclass
class PriceAnalysis:
    current_price: float
    min_price: float
    max_price: float
    avg_price: float
    target_price: float
    is_target_reached: bool
    is_all_time_low: bool
    discount_vs_avg: float


class PriceAnalyzer:
    @staticmethod
    def analyze(current_price: float, history: List[float], target_price: float) -> PriceAnalysis:
        all_prices = history + [current_price] if history else [current_price]
        min_p = min(all_prices)
        max_p = max(all_prices)
        avg_p = round(sum(all_prices) / len(all_prices), 2)

        discount_vs_avg = round(((avg_p - current_price) / avg_p) * 100, 1) if avg_p > 0 else 0.0

        return PriceAnalysis(
            current_price=current_price,
            min_price=min_p,
            max_price=max_p,
            avg_price=avg_p,
            target_price=target_price,
            is_target_reached=current_price <= target_price,
            is_all_time_low=current_price <= min_p and len(all_prices) > 1,
            discount_vs_avg=discount_vs_avg,
        )
