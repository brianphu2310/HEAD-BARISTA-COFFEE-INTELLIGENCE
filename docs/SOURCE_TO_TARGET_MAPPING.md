# Source-to-Target Mapping

Maps the three sources the repo already contains to the warehouse built by `python -m pipeline`
(`pipeline/extract.py` -> `validate.py` -> `transform.py` -> `load.py`). Model: [DATA_MODEL.md](DATA_MODEL.md). Column meanings: [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

## Sources

| ID | Source | Content |
|---|---|---|
| S1 | `coffee_dataset.csv` | 32 coffee beans |
| S2 | `data/Coffee_Brewing_Dashboard_Final.xlsx` (first sheet) | 13 brewing methods (title block, then header row) |
| S3 | `sql/Beans_And_Methods_Streamlit_Dataset.sql` | CTEs `coffee_data`, `brewing_methods` (reconciliation) and `method_mapping` (bean label -> canonical method) |

## S1 beans -> target

| Source column | Target | Rule |
|---|---|---|
| `Coffee_Name` | `dim_coffee.coffee_name` | Trim; de-duplicate; surrogate `coffee_key` ordered by name. |
| `Latitude`, `Longitude` | `dim_coffee.latitude`, `.longitude` | Float. |
| (derived) | `dim_coffee.latitude_band` | abs(latitude) < 10 -> `0-10`; < 20 -> `10-20`; else `20+`. |
| `Origin` | `dim_origin.origin_country` -> `fact_coffee_rating.origin_key` | Distinct values, surrogate key. |
| (derived) | `dim_origin.continent` | Lookup `ORIGIN_REF` in `validate.py`. |
| `Roast_Level` | `dim_roast.roast_level` -> `fact_coffee_rating.roast_key` | Distinct values. |
| (derived) | `dim_roast.roast_order` | Light 1, Medium 2, Dark 3; key assigned in that order. |
| `Processing_Method` | `dim_process.processing_method` -> `fact_coffee_rating.process_key` | Distinct values. |
| `Brew_Method` | `fact_coffee_rating.served_brew_method` (as given) and `fact_coffee_rating.brew_method_key` (via S3 `method_mapping`) | Label is mapped to the canonical method name, then to `dim_brew_method.brew_method_key`. |
| `Acidity`, `Body`, `Sweetness` | `fact_coffee_rating.acidity_level`, `body_level`, `sweetness_level` | Kept as text labels. |
| (derived) | `fact_coffee_rating.acidity_ord`, `body_ord`, `sweetness_ord` | Low 1, Medium 2, High 3 (Light 1, Full 3 for body); analyst-defined. |
| `Flavor_Notes` | `dim_flavor.flavor_note` + `bridge_coffee_flavor` | Split on comma, trim, lower-case; one bridge row per distinct (coffee, note) - many-to-many. |
| (derived) | `fact_coffee_rating.flavor_note_count` | Number of notes in the list. |
| `Rating` | `fact_coffee_rating.rating` | Int. |
| (derived) | `fact_coffee_rating.rating_band` | >= 90 -> `90+`; >= 85 -> `85-89`; else `Below 85`. |

## S2 methods -> `dim_brew_method`

| Source column (workbook header) | Target column | Rule |
|---|---|---|
| Method | `method_name` | Natural key; surrogate `brew_method_key` ordered by name. |
| Brew Time (min) | `brew_time_min` | Float. |
| Caffeine (mg) | `caffeine_mg` | Int. |
| Antioxidant Rank (1-5) | `antioxidant_rank` | Int. |
| Acidity (1-10), Bitterness (1-10), Body (1-10) | `acidity_score`, `bitterness_score`, `body_score` | Int. |
| Complexity | `complexity` | Text. |
| Recommended Equipment | `equipment` | Text. |
| Quick Brewing Guide | `quick_guide` | Text. |
| Primary Taste | `primary_taste` | Text. |
| Caffeine Level | (not loaded) | Emoji prefix stripped on read, but `caffeine_level` is re-derived from `caffeine_mg` via `validate.caffeine_level` so one rule drives it. |
| (derived) | `sleep_impact` | `validate.sleep_impact(caffeine_mg)`. |
| Score Index | `score_index_excel` | Float, kept for traceability to the workbook. |

## S3 SQL script -> use

| Part | Use |
|---|---|
| `method_mapping` CTE | Single origin of the bean-label -> canonical-method mapping; one exact duplicate row is removed in `transform.py`. |
| `coffee_data`, `brewing_methods` CTEs | Parsed and reconciled against S1 and S2; differences are reported in [DATA_QUALITY.md](DATA_QUALITY.md). Not loaded separately. |

## Load order and integrity

`dim_origin`, `dim_roast`, `dim_process`, `dim_brew_method`, `dim_coffee`, `dim_flavor` -> `fact_coffee_rating` -> `bridge_coffee_flavor`. Foreign keys enforced; row counts audited.

## Known limits

- The repo does not document where the 32 bean rows or their `Rating` values came from; the mapping preserves them as given.
- Brew-method attributes in S2 come from hard-coded dictionaries in the scraping notebook and were not re-verified here.
- No time or customer dimension exists in any source.
