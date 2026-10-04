# Ingestion

Reusable ingestion modules ported from `notebooks/BREWING_METHODS_SCRAPING.ipynb`. They sit upstream of the existing pipeline: they write raw CSVs under `data/raw/`; the committed files that `pipeline/` reads are unchanged and the pipeline still makes no network calls.

## Status (read first)

- **Parser verified on fixtures only.** The parser unit tests use small hand-written HTML fixtures (`tests/fixtures/`, labelled as not captured pages) that mimic the selectors the notebook uses.
- **Live run not verified in CI.** CI has no network access to the target sites, and the live fetch has never been run from this module. The notebook's selectors may no longer match the live markup.
- **Check the site's terms of use before running.** The fetcher reads `robots.txt` and stops if the URL is disallowed, but that is not a substitute for reading the terms.
- **For personal / portfolio use only.** Do not redistribute scraped content.
- Not wired into CI as a live job, and not part of `python -m pipeline`.

## Sources and selectors ported

- Wikipedia: the notebook's 13 method URLs. `div#mw-content-text`; description = first `<p>` over 100 characters not starting with "Coordinates" (first 500 chars); brew time = first match of the notebook's three regexes; caffeine = `NN mg ... caffeine`.
- Healthline caffeine article: every `<table>` row with at least two cells; average of the numbers in the second cell.
- Perfect Daily Grind guide: `<h2>`/`<h3>` headings containing a method keyword, text of following siblings up to the next heading; brew-time regex and Low/Medium/High complexity hint from keywords. Deviation: the notebook's brew-time regex contains a typo (`S]*`) that makes it almost never match; corrected to `[\s-]*`.
- National Coffee Association guide: `<h2>`/`<h3>`/`<h4>` headings containing a method keyword and the following siblings.
- Not ingestion, so not ported: the notebook's hard-coded master dictionaries (brew time, caffeine, antioxidant rank, sensory scores, equipment, guides). They are curated values, not scraped.
- Parser is BeautifulSoup `html.parser`; the notebook used `lxml`.

## Design

| Concern | Where | How |
|---|---|---|
| Fetching | `ingestion/fetch.py` | `PoliteFetcher.get_html(url)` |
| Parsing (pure) | `ingestion/brewing_methods.py` | `parse_wikipedia_method`, `parse_healthline_caffeine`, `parse_pdg_methods`, `parse_nca_methods` |
| Orchestration + CLI | `ingestion/brewing_methods.py` | `scrape_source(...)`, `python -m ingestion.brewing_methods [--sources ...]` |
| robots.txt | `ingestion/fetch.py` | `urllib.robotparser`; 404 = allowed, 401/403 or unreachable/5xx = treated as disallowed; `RobotsDisallowed` aborts the run (CLI exit code 3, nothing written) |
| Identifying User-Agent | `ingestion/fetch.py`, module constant | Names the project and repo; override with `--user-agent` |
| Rate limit | `PoliteFetcher` | `min_interval` must be >= 1 s (enforced); also applies to robots.txt requests |
| Retries | `PoliteFetcher` | Network errors and HTTP 429/500/502/503/504; exponential backoff (2 s, 4 s, ...), honours numeric `Retry-After` |
| Raw HTML cache | `data/raw_html/` (git-ignored) | One file per URL (SHA-256 of the URL); a cache hit makes no request |
| Output | `data/raw/brewing_<source>.csv` (`--out` is a directory) | CSV with `scraped_at` (UTC ISO) and `source_url` |
| Logging | `logging` | INFO by default, `-v` for debug |

## Tests (offline)

- `tests/test_ingestion_fetch.py`: robots allow/disallow/404/403/unreachable, one robots fetch per host, User-Agent header, rate-limit spacing, retry/backoff/give-up, `Retry-After`, cache. HTTP is mocked with a fake session and a fake clock, so the tests neither sleep nor use the network.
- `tests/test_ingestion_*.py` (module tests): parsers on hand-written fixtures in `tests/fixtures/` (see its README: minimal, written to match the notebook's selectors, **not captured pages**), plus the assembly step with a stub fetcher and the CLI's robots abort.

These tests show the code does what it says on markup written to match the notebook. They say nothing about whether the live sites still serve that markup.
