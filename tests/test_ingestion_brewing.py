"""Brewing-methods ingestion: parsers on hand-written fixtures (tests/fixtures/README.md) + mocked scrape."""
import csv
from pathlib import Path

import pytest

from ingestion import brewing_methods as bm
from ingestion.fetch import FetchError, RobotsDisallowed

FX = Path(__file__).parent / "fixtures"


def fx(name):
    return (FX / name).read_text(encoding="utf-8")


def test_wikipedia_description_time_and_caffeine():
    r = bm.parse_wikipedia_method(fx("wikipedia_method.html"))
    assert r["description"].startswith("Test brew is a made-up method")
    assert len(r["description"]) <= 500
    assert r["brew_time_scraped"] == "2 min"  # the notebook's 2nd pattern; "25 to 30 seconds" is not matched
    assert r["caffeine_scraped_mg"] == 64


def test_wikipedia_first_time_pattern_wins_and_missing_content():
    html = '<div id="mw-content-text"><p>' + "x" * 120 + " brew 3 to 5 minutes.</p></div>"
    assert bm.parse_wikipedia_method(html)["brew_time_scraped"] == "3 to 5 min"
    assert bm.parse_wikipedia_method(fx("wikipedia_no_content.html")) == {}


def test_healthline_rows_average_and_clean_text():
    rows = bm.parse_healthline_caffeine(fx("healthline_table.html"))
    assert rows == [
        {"drink_name": "brewed coffee 8 oz", "caffeine_range_text": "70-140 mg", "caffeine_avg_mg": 105},
        {"drink_name": "test espresso", "caffeine_range_text": "64 mg", "caffeine_avg_mg": 64},
    ]


def test_pdg_headings_complexity_and_time():
    rows = bm.parse_pdg_methods(fx("pdg_guide.html"))
    assert [r["method_scraped"] for r in rows] == ["Test Espresso", "French Press"]
    assert rows[0]["complexity_hint"] == "Low"
    assert rows[0]["brew_time_scraped"] == "30 second"  # regex typo from the notebook fixed, see module
    assert rows[1]["complexity_hint"] == "Medium"  # "practice"/"technique" before any High keyword
    assert rows[1]["brew_time_scraped"] == "4 minute"
    assert "Bye" not in rows[1]["content_snippet"]  # stops at next h2


def test_nca_sections_stop_at_next_heading():
    rows = bm.parse_nca_methods(fx("nca_methods.html"))
    assert [r["method_section"] for r in rows] == ["Drip Brewers", "Cold Brew"]
    assert rows[0]["guide_snippet"] == "Automatic and easy. Second paragraph."
    assert rows[1]["guide_snippet"] == "Steep overnight."


def test_wikipedia_url_table_matches_notebook():
    assert len(bm.WIKI_BREW_URLS) == 13
    assert bm.WIKI_BREW_URLS["Cold Drip"] == bm.WIKI_BREW_URLS["Cold Brew"]  # same page, as in the notebook


class StubFetcher:
    def __init__(self, pages, errors=None):
        self.pages, self.errors = pages, errors or {}

    def get_html(self, url):
        if url in self.errors:
            raise self.errors[url]
        return self.pages[url]


def test_scrape_wikipedia_adds_source_url_and_timestamp_and_skips_failures():
    pages = {u: fx("wikipedia_method.html") for u in bm.WIKI_BREW_URLS.values()}
    bad = bm.WIKI_BREW_URLS["Lungo"]
    rows = bm.scrape_source(StubFetcher(pages, {bad: FetchError("boom")}), "wikipedia")
    assert len(rows) == 12 and "Lungo" not in {r["method"] for r in rows}
    assert all(r["source"] == "Wikipedia" and r["source_url"] in bm.WIKI_BREW_URLS.values() and r["scraped_at"]
               for r in rows)


def test_scrape_other_sources_and_csv(tmp_path):
    f = StubFetcher({bm.HEALTHLINE_URL: fx("healthline_table.html"), bm.PDG_URL: fx("pdg_guide.html"),
                     bm.NCA_URL: fx("nca_methods.html")})
    for src, n in [("healthline", 2), ("pdg", 2), ("nca", 2)]:
        rows = bm.scrape_source(f, src)
        assert len(rows) == n
        path = bm.write_csv(rows, src, tmp_path)
        got = list(csv.DictReader(path.open(encoding="utf-8")))
        assert list(got[0])[:3] == ["source", "source_url", "scraped_at"] and got[0]["scraped_at"]


def test_unknown_source_and_robots_abort(tmp_path, monkeypatch):
    with pytest.raises(ValueError):
        bm.scrape_source(StubFetcher({}), "nope")

    def deny(self, url):
        raise RobotsDisallowed("robots.txt disallows")

    monkeypatch.setattr("ingestion.fetch.PoliteFetcher.get_html", deny)
    assert bm.main(["--out", str(tmp_path / "o"), "--cache-dir", str(tmp_path / "c")]) == 3
    assert not (tmp_path / "o").exists()
