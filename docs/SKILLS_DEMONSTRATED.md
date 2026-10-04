# Skills Demonstrated

Every path below exists in this repo and is exercised by the tests or CI.

| Skill | Where to see it |
|---|---|
| SQL: CTEs, joins (incl. LEFT JOIN, many-to-many via bridge), aggregation, `CASE` pivots | [`sql/analysis/05_flavour_notes_lift.sql`](../sql/analysis/05_flavour_notes_lift.sql), [`06_method_caffeine_ladder.sql`](../sql/analysis/06_method_caffeine_ladder.sql), [`07_latitude_band_by_roast.sql`](../sql/analysis/07_latitude_band_by_roast.sql), [`08_acidity_fit_by_method.sql`](../sql/analysis/08_acidity_fit_by_method.sql) |
| SQL: window functions (`RANK`, `DENSE_RANK`, `ROW_NUMBER`, `NTILE`, `PERCENT_RANK`, `CUME_DIST`, `LAG`, `FIRST_VALUE`, running totals) | [`01_origin_leaderboard.sql`](../sql/analysis/01_origin_leaderboard.sql), [`02_top_coffees_per_method.sql`](../sql/analysis/02_top_coffees_per_method.sql), [`04_rating_distribution.sql`](../sql/analysis/04_rating_distribution.sql), [`06_method_caffeine_ladder.sql`](../sql/analysis/06_method_caffeine_ladder.sql), [`09_best_coffee_per_origin.sql`](../sql/analysis/09_best_coffee_per_origin.sql), [`10_process_by_continent.sql`](../sql/analysis/10_process_by_continent.sql) |
| Existing PostgreSQL work (schema, CTE-based dataset, recommender function in README) | [`sql/Coffee_beans_dataset.sql`](../sql/Coffee_beans_dataset.sql), [`sql/Beans_And_Methods_Streamlit_Dataset.sql`](../sql/Beans_And_Methods_Streamlit_Dataset.sql) |
| Dimensional modelling (star schema, bridge table, surrogate keys, grain) | [`pipeline/schema.sql`](../pipeline/schema.sql), [`docs/DATA_MODEL.md`](DATA_MODEL.md) |
| ETL in Python from three heterogeneous sources (CSV, Excel with title block, SQL script parsed with regex) | [`pipeline/extract.py`](../pipeline/extract.py), [`transform.py`](../pipeline/transform.py), [`load.py`](../pipeline/load.py), [`__main__.py`](../pipeline/__main__.py) |
| Data quality (nulls, duplicates, ranges, domains, referential, cross-source reconciliation, warnings for known quirks) | [`pipeline/validate.py`](../pipeline/validate.py), report in [`docs/DATA_QUALITY.md`](DATA_QUALITY.md) |
| Data documentation (generated dictionary with provenance notes, ER diagram) | [`pipeline/docgen.py`](../pipeline/docgen.py), [`docs/DATA_DICTIONARY.md`](DATA_DICTIONARY.md), [`docs/DATA_MODEL.md`](DATA_MODEL.md) |
| Reproducible query outputs | [`sql/run_queries.py`](../sql/run_queries.py), [`docs/query_results/`](query_results/) |
| Testing (pytest: defect injection, determinism, query results checked against pandas, docs freshness; Streamlit smoke test) | [`tests/test_pipeline.py`](../tests/test_pipeline.py), [`tests/test_queries.py`](../tests/test_queries.py), [`tests/test_app_smoke.py`](../tests/test_app_smoke.py) |
| CI (tests, end-to-end run, generated-docs freshness gate) | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |
| Web scraping (existing notebook, documented only) | [`notebooks/BREWING_METHODS_SCRAPING.ipynb`](../notebooks/BREWING_METHODS_SCRAPING.ipynb): not re-run or modified here; the pipeline starts from its committed outputs |
| Reusable, polite web ingestion: `robots.txt` check, identifying User-Agent, rate limiting, retries with backoff, on-disk HTML cache, pure parsers separated from fetching, CSV with timestamp and source URL. Parsers verified on hand-written fixtures; live run on a GitHub runner returned Wikipedia 13 / Healthline 3 / NCA 5 rows, one source blocked (see `docs/LIVE_RUN.md`) | [`ingestion/fetch.py`](../ingestion/fetch.py), [`ingestion/brewing_methods.py`](../ingestion/brewing_methods.py), [`docs/INGESTION.md`](INGESTION.md) |
| Offline tests for network code (mocked HTTP, fake clock, fixtures) | [`tests/test_ingestion_fetch.py`](../tests/test_ingestion_fetch.py), [`tests/test_ingestion_brewing.py`](../tests/test_ingestion_brewing.py), [`tests/fixtures/`](../tests/fixtures/) |
| App / BI delivery | Streamlit app [`app.py`](../app.py); Tableau and Colab links in the [README](../README.md); Power BI report with DAX measures and a star-schema model in [`powerbi/barista_dashboard.pbix`](../powerbi/barista_dashboard.pbix) |

Not claimed: no verified live ingestion (the ingestion modules have not been run against the live sites), no API ingestion, no orchestration tool, no cloud warehouse, no statistical modelling.
