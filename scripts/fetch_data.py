#!/usr/bin/env python3
"""Fetch Japan GDP series from the World Bank API and regenerate data files.

Usage: python3 scripts/fetch_data.py
Outputs: data/japan_gdp.json, data/japan_gdp.csv, assets/data.js
Indicators (World Bank WDI, country=JPN, 1960-2025):
  NY.GDP.MKTP.CD  GDP (current US$)
  NY.GDP.MKTP.CN  GDP (current LCU, yen)
  NY.GDP.MKTP.KD  GDP (constant 2015 US$)
  NY.GDP.MKTP.KD.ZG  GDP growth (annual %)
  NY.GDP.PCAP.CD  GDP per capita (current US$)
  SP.POP.TOTL     Population
"""
import csv
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDICATORS = {
    "gdp_usd": "NY.GDP.MKTP.CD",
    "gdp_yen": "NY.GDP.MKTP.CN",
    "gdp_const": "NY.GDP.MKTP.KD",
    "growth": "NY.GDP.MKTP.KD.ZG",
    "gdp_per_capita": "NY.GDP.PCAP.CD",
    "pop": "SP.POP.TOTL",
}


def fetch(code: str) -> dict:
    url = (
        f"https://api.worldbank.org/v2/country/JPN/indicator/{code}"
        "?format=json&per_page=200&date=1960:2025"
    )
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.load(resp)
    return {int(r["date"]): r["value"] for r in data[1] if r["value"] is not None}


def main() -> None:
    series = {name: fetch(code) for name, code in INDICATORS.items()}
    base_const = series["gdp_const"][1960]
    records = []
    for year in sorted(series["gdp_usd"]):
        gdp, yen = series["gdp_usd"][year], series["gdp_yen"][year]
        records.append(
            {
                "year": year,
                "gdp_usd_trillion": round(gdp / 1e12, 4),
                "gdp_yen_trillion": round(yen / 1e12, 2),
                "gdp_const_usd_trillion": round(series["gdp_const"][year] / 1e12, 4),
                "growth_pct": round(series["growth"][year], 3)
                if year in series["growth"]
                else None,
                "gdp_per_capita_usd": round(series["gdp_per_capita"][year], 1),
                "population_million": round(series["pop"][year] / 1e6, 3),
                "implied_yen_per_usd": round(yen / gdp, 1),
                "real_index_1960_100": round(series["gdp_const"][year] / base_const * 100, 1),
            }
        )
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "data" / "japan_gdp.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2)
    )
    with open(ROOT / "data" / "japan_gdp.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    (ROOT / "assets" / "data.js").write_text(
        "window.JAPAN_GDP = " + json.dumps(records, ensure_ascii=False) + ";\n"
    )
    print(f"wrote {len(records)} records ({records[0]['year']}-{records[-1]['year']})")


if __name__ == "__main__":
    main()
