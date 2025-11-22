import os
import json
from typing import Any, Dict

def generate_summary_from_data(payload: Dict[str, Any], mode: str = "single") -> str:
    """Generate a natural-language summary using OpenAI if available.

    payload: a dict containing relevant data (chartData, tableData, localities)
    mode: one of 'single', 'comparison', 'price_growth'

    If OpenAI is not configured, returns a concise summary based on the
    provided payload using a simple fallback.
    """
    # Try to import openai and call the API. If anything fails, fall back.
    try:
        import openai
    except Exception:
        return _fallback_summary(payload, mode)

    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_APIKEY")
    if not api_key:
        return _fallback_summary(payload, mode)

    openai.api_key = api_key

    # Build a concise prompt from payload
    try:
        system = (
            "You are a helpful assistant that summarizes real-estate datasets. "
            "Given structured JSON data (years, prices, demand, table rows), produce a short (2-3 sentence) summary that highlights trends, recent demand, and price growth."
        )

        user_msg = (
            f"Mode: {mode}\nData:\n{json.dumps(payload, ensure_ascii=False, indent=2)}\n\n"
            "Write a concise plain-text summary (2-3 sentences)."
        )

        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=150,
            temperature=0.4,
        )

        text = resp["choices"][0]["message"]["content"].strip()
        return text
    except Exception:
        return _fallback_summary(payload, mode)


def _fallback_summary(payload: Dict[str, Any], mode: str) -> str:
    # Simple deterministic fallback: use data to create a short summary
    try:
        if mode == "comparison":
            locs = payload.get("localities", [])
            chart = payload.get("chartData", {})
            if len(locs) >= 2:
                a, b = locs[0], locs[1]
                a_prices = chart.get(a, {}).get("price", [])
                b_prices = chart.get(b, {}).get("price", [])
                a_latest = a_prices[-1] if a_prices else None
                b_latest = b_prices[-1] if b_prices else None
                return f"{a} shows a latest price of {a_latest} while {b} shows {b_latest}. {a} has shown steady growth compared to {b}."
        elif mode == "price_growth":
            chart = payload.get("chartData", {})
            prices = chart.get("price", [])
            years = chart.get("year", [])
            if prices and years:
                return f"Price moved from {prices[0]} in {years[0]} to {prices[-1]} in {years[-1]}, indicating growth over the period."
        else:
            chart = payload.get("chartData", {})
            prices = chart.get("price", [])
            demand = chart.get("demand", [])
            if prices:
                return f"Prices range from {min(prices)} to {max(prices)}. Demand ranges from {min(demand) if demand else 'N/A'} to {max(demand) if demand else 'N/A'}."
    except Exception:
        pass
    return "No detailed summary available."
