"""Brewing-methods ingestion, ported from notebooks/BREWING_METHODS_SCRAPING.ipynb.

Only the four sources the notebook scrapes are ported, with the same URLs and selectors:
  * wikipedia   13 method pages (``div#mw-content-text``: first <p> longer than 100 chars, a brew-time
                regex, a caffeine-mg regex)
  * healthline  https://www.healthline.com/nutrition/how-much-caffeine-in-coffee  (every <table> row)
  * pdg         Perfect Daily Grind guide (<h2>/<h3> headings naming a method + following siblings)
  * nca         National Coffee Association brewing methods (<h2>/<h3>/<h4> + following siblings)
The notebook's hard-coded master dictionaries (brew time, caffeine, sensory scores, ...) are curated
data, not scraped, and are not part of ingestion.

Usage:  python -m ingestion.brewing_methods --out data/raw   (writes brewing_<source>.csv per source)

Personal / portfolio use only. Check each site's terms of use before running a live fetch.
"""
from __future__ import annotations

import argparse
import csv
import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

from .fetch import FetchError, PoliteFetcher, RobotsDisallowed

log = logging.getLogger("ingestion.brewing_methods")

USER_AGENT = (
    "head-barista-portfolio-ingest/0.1 (personal portfolio project; "
    "https://github.com/brianphu2310/head-barista-coffee-intelligence)"
)

WIKI_BREW_URLS = {  # verbatim from the notebook
    "Espresso": "https://en.wikipedia.org/wiki/Espresso",
    "Ristretto": "https://en.wikipedia.org/wiki/Ristretto",
    "Lungo": "https://en.wikipedia.org/wiki/Lungo",
    "AeroPress": "https://en.wikipedia.org/wiki/AeroPress",
    "Moka Pot": "https://en.wikipedia.org/wiki/Moka_pot",
    "Pour Over": "https://en.wikipedia.org/wiki/Pour-over_coffee",
    "French Press": "https://en.wikipedia.org/wiki/French_press",
    "Turkish": "https://en.wikipedia.org/wiki/Turkish_coffee",
    "Cold Brew": "https://en.wikipedia.org/wiki/Cold_brew_coffee",
    "Siphon": "https://en.wikipedia.org/wiki/Vacuum_coffee_maker",
    "Vietnamese Phin": "https://en.wikipedia.org/wiki/Vietnamese_iced_coffee",
    "Cold Drip": "https://en.wikipedia.org/wiki/Cold_brew_coffee",
    "Batch Brew": "https://en.wikipedia.org/wiki/Drip_coffee_maker",
}
HEALTHLINE_URL = "https://www.healthline.com/nutrition/how-much-caffeine-in-coffee"
PDG_URL = "https://perfectdailygrind.com/2019/10/a-guide-to-every-coffee-brewing-method/"
NCA_URL = "https://www.ncausa.org/About-Coffee/Brewing-Methods"

PDG_KEYWORDS = ["espresso", "ristretto", "lungo", "aeropress", "moka", "french press",
                "pour over", "pour-over", "cold brew", "turkish", "siphon", "vietnamese"]
NCA_KEYWORDS = ["drip", "french", "espresso", "cold", "pour", "moka", "turkish", "aeropress", "siphon"]

FIELDS = {
    "wikipedia": ["method", "description", "brew_time_scraped", "caffeine_scraped_mg"],
    "healthline": ["drink_name", "caffeine_range_text", "caffeine_avg_mg"],
    "pdg": ["method_scraped", "brew_time_scraped", "complexity_hint", "content_snippet"],
    "nca": ["method_section", "guide_snippet"],
}
PROVENANCE = ["source", "source_url", "scraped_at"]


# ---- pure parsers --------------------------------------------------------------------------
def clean_text(text: str) -> str:
    """Notebook's clean_text: collapse whitespace, strip [ ] ( ) *."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"[\[\]\(\)\*]", "", text)


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def parse_wikipedia_method(html: str) -> dict:
    """description (<=500 chars), brew_time_scraped, caffeine_scraped_mg; keys only if found."""
    result: dict = {}
    content = _soup(html).find("div", {"id": "mw-content-text"})
    if not content:
        return result
    for p in content.find_all("p", recursive=True):
        text = clean_text(p.get_text())
        if len(text) > 100 and not text.startswith("Coordinates"):
            result["description"] = text[:500]
            break
    full_text = content.get_text().lower()
    for pattern in (r"(\d+)\s*(?:to|–|-)\s*(\d+)\s*(?:min|minute)",
                    r"(\d+(?:\.\d+)?)\s*(?:min|minute|minutes)",
                    r"(\d+)\s*(?:second|sec|seconds)"):
        m = re.search(pattern, full_text)
        if m:
            result["brew_time_scraped"] = m.group(0)
            break
    m = re.search(r"(\d{2,4})\s*(mg|milligrams?)\s*(?:of\s*)?caffeine", full_text, re.IGNORECASE)
    if m:
        result["caffeine_scraped_mg"] = int(m.group(1))
    return result


def parse_healthline_caffeine(html: str) -> list[dict]:
    """Every table row with >= 2 cells and a number in the 2nd cell; avg of all numbers found."""
    out = []
    for table in _soup(html).find_all("table"):
        for row in table.find_all("tr"):
            cells = row.find_all(["th", "td"])
            if len(cells) >= 2:
                drink = clean_text(cells[0].get_text()).lower()
                value = clean_text(cells[1].get_text())
                numbers = re.findall(r"\d+", value)
                if numbers:
                    out.append({"drink_name": drink, "caffeine_range_text": value,
                                "caffeine_avg_mg": int(sum(int(n) for n in numbers) / len(numbers))})
    return out


def _following_text(heading, stop_tags: tuple[str, ...]) -> str:
    content = ""
    for sib in heading.find_next_siblings():
        if sib.name in stop_tags:
            break
        content += " " + sib.get_text()
    return clean_text(content)


def parse_pdg_methods(html: str) -> list[dict]:
    out = []
    for h in _soup(html).find_all(["h2", "h3"]):
        title = clean_text(h.get_text())
        if not any(kw in title.lower() for kw in PDG_KEYWORDS):
            continue
        content = _following_text(h, ("h2", "h3"))
        # The notebook's pattern has a typo ("S]*" instead of "[\s-]*") that requires a literal "S" and so
        # almost never matches. Fixed here to the evident intent: "N [to M] unit".
        m = re.search(r"(\d+)[\s-]*(to|–|-)?[\s-]*(\d+)?\s*(minute|min|second|sec|hour|hr)", content, re.IGNORECASE)
        low = content.lower()
        complexity = None
        if any(w in low for w in ["beginner", "easy", "simple"]):
            complexity = "Low"
        elif any(w in low for w in ["intermediate", "practice", "technique"]):
            complexity = "Medium"
        elif any(w in low for w in ["expert", "difficult", "advanced", "professional"]):
            complexity = "High"
        out.append({"method_scraped": title, "brew_time_scraped": m.group(0) if m else None,
                    "complexity_hint": complexity, "content_snippet": content[:300]})
    return out


def parse_nca_methods(html: str) -> list[dict]:
    out = []
    for h in _soup(html).find_all(["h2", "h3", "h4"]):
        title = clean_text(h.get_text())
        if not any(kw in title.lower() for kw in NCA_KEYWORDS):
            continue
        out.append({"method_section": title,
                    "guide_snippet": _following_text(h, ("h2", "h3", "h4"))[:400]})
    return out


# ---- fetch + assemble ----------------------------------------------------------------------
def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _stamp(rows: list[dict], source: str, url: str) -> list[dict]:
    t = _now()
    return [{**r, "source": source, "source_url": url, "scraped_at": t} for r in rows]


def _fetch(fetcher, url):
    try:
        return fetcher.get_html(url)
    except RobotsDisallowed:
        raise
    except FetchError as exc:
        log.error("skipping %s: %s", url, exc)
        return None


def scrape_source(fetcher: PoliteFetcher, source: str) -> list[dict]:
    """Rows for one source. RobotsDisallowed propagates; other fetch failures skip the page."""
    rows: list[dict] = []
    if source == "wikipedia":
        for method, url in WIKI_BREW_URLS.items():
            html = _fetch(fetcher, url)
            if html is not None:
                rows += _stamp([{"method": method, **parse_wikipedia_method(html)}], "Wikipedia", url)
    elif source == "healthline":
        html = _fetch(fetcher, HEALTHLINE_URL)
        if html is not None:
            rows = _stamp(parse_healthline_caffeine(html), "Healthline", HEALTHLINE_URL)
    elif source == "pdg":
        html = _fetch(fetcher, PDG_URL)
        if html is not None:
            rows = _stamp(parse_pdg_methods(html), "Perfect Daily Grind", PDG_URL)
    elif source == "nca":
        html = _fetch(fetcher, NCA_URL)
        if html is not None:
            rows = _stamp(parse_nca_methods(html), "National Coffee Association", NCA_URL)
    else:
        raise ValueError(f"unknown source {source!r}")
    log.info("%s: %d rows", source, len(rows))
    return rows


def write_csv(rows: list[dict], source: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"brewing_{source}.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=PROVENANCE + FIELDS[source], extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="data/raw", type=Path, help="output directory")
    ap.add_argument("--cache-dir", default="data/raw_html", type=Path)
    ap.add_argument("--sources", nargs="+", choices=list(FIELDS), default=list(FIELDS))
    ap.add_argument("--min-interval", type=float, default=2.0, help="seconds between requests (>= 1)")
    ap.add_argument("--user-agent", default=USER_AGENT)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    fetcher = PoliteFetcher(args.user_agent, args.cache_dir, args.min_interval)
    results: dict[str, list[dict]] = {}
    try:
        for src in args.sources:
            results[src] = scrape_source(fetcher, src)
    except RobotsDisallowed as exc:
        log.error("%s. Aborting; nothing written.", exc)
        return 3
    for src, rows in results.items():
        if rows:
            log.info("wrote %s", write_csv(rows, src, args.out))
        else:
            log.warning("%s: no rows, no file written", src)
    return 0 if any(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
