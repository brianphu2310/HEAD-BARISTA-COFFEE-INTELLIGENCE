"""Generate docs/DATA_DICTIONARY.md from the live warehouse (types, examples, observed allowed values).

Descriptions are written by hand in DESCRIPTIONS; the generator fails if a column has no description,
so the dictionary can never silently drift from the schema.  Usage: python -m pipeline.docgen
"""
import sqlite3
from pathlib import Path

from .load import DB_PATH

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "DATA_DICTIONARY.md"

DESCRIPTIONS = {
    "dim_origin": {
        "origin_key": "Surrogate key (alphabetical by country).",
        "origin_country": "Country of origin as written in `coffee_dataset.csv` (`Origin`).",
        "continent": "Analyst-defined continent grouping (`ORIGIN_REF` in pipeline/validate.py); not in the source data.",
    },
    "dim_roast": {
        "roast_key": "Surrogate key, ordered light to dark.",
        "roast_level": "Roast level from the source (`Roast_Level`).",
        "roast_order": "1 = Light, 2 = Medium, 3 = Dark (for ordering).",
    },
    "dim_process": {
        "process_key": "Surrogate key (alphabetical).",
        "processing_method": "Green-coffee processing method from the source (`Processing_Method`).",
    },
    "dim_brew_method": {
        "brew_method_key": "Surrogate key (alphabetical by method).",
        "method_name": "Canonical brewing method (workbook `Method`).",
        "brew_time_min": "Brew time in minutes (Cold Drip 480 and Cold Brew 1080 are hours-long methods).",
        "caffeine_mg": "Caffeine in mg per serving as stored in the workbook (notebook comments cite USDA / Mayo Clinic; not re-verified here).",
        "antioxidant_rank": "Antioxidant rank 1-5 from the workbook (higher = more antioxidants, per notebook comment).",
        "acidity_score": "Acidity 1-10 from the workbook (notebook comment: from specialty coffee associations; not re-verified here).",
        "bitterness_score": "Bitterness 1-10 from the workbook.",
        "body_score": "Body 1-10 from the workbook.",
        "complexity": "Complexity label (Low/Medium/High) from the workbook.",
        "equipment": "Recommended equipment from the workbook.",
        "quick_guide": "One-line brewing guide from the workbook.",
        "primary_taste": "Comma-separated primary taste descriptors from the workbook.",
        "caffeine_level": "Derived from caffeine_mg: Low <= 75; Medium <= 150; High > 150 (same rule as the SQL script).",
        "sleep_impact": "Derived from caffeine_mg: <= 75 Won't disrupt sleep; <= 200 May affect sleep; else Avoid after 2 PM (same rule as the SQL script).",
        "score_index_excel": "`Score Index` column of the workbook, kept for lineage. It disagrees with the SQL script's Score_Index and its formula is undocumented, so no query uses it.",
    },
    "dim_coffee": {
        "coffee_key": "Surrogate key (alphabetical by coffee name).",
        "coffee_name": "Coffee name from the source (`Coffee_Name`).",
        "latitude": "Latitude in decimal degrees from the source.",
        "longitude": "Longitude in decimal degrees from the source.",
        "latitude_band": "Derived band of absolute latitude in degrees: 0-10 (< 10), 10-20 (10 to < 20), 20+ (>= 20).",
    },
    "dim_flavor": {
        "flavor_key": "Surrogate key (alphabetical).",
        "flavor_note": "One lower-cased flavour token split from `Flavor_Notes`.",
    },
    "fact_coffee_rating": {
        "coffee_key": "PK and FK to dim_coffee; one fact row per coffee listing.",
        "origin_key": "FK to dim_origin.",
        "roast_key": "FK to dim_roast.",
        "process_key": "FK to dim_process.",
        "brew_method_key": "FK to dim_brew_method, found by mapping the bean's brew-method label through the SQL script's method_mapping.",
        "served_brew_method": "Brew-method label exactly as written in the beans data (e.g. Chemex, Clever Dripper), before mapping.",
        "acidity_level": "Bean acidity from the source (`Acidity`).",
        "body_level": "Bean body description from the source (`Body`).",
        "sweetness_level": "Bean sweetness from the source (`Sweetness`).",
        "acidity_ord": "Ordinal encoding of acidity_level: Low=1, Medium=2, High=3.",
        "body_ord": "Ordinal encoding of body_level: Light=1, Medium=2, Full=3.",
        "sweetness_ord": "Ordinal encoding of sweetness_level: Low=1, Medium=2, High=3.",
        "flavor_note_count": "Number of flavour tokens in `Flavor_Notes`.",
        "rating": "Integer rating from the source (`Rating`); the rating methodology is not documented in the repo.",
        "rating_band": "Derived: 90+ for rating >= 90; 85-89; Below 85.",
    },
    "bridge_coffee_flavor": {
        "coffee_key": "FK to dim_coffee (part of PK).",
        "flavor_key": "FK to dim_flavor (part of PK).",
    },
    "vw_coffee_flat": {
        "coffee_name": "dim_coffee.coffee_name.", "origin": "dim_origin.origin_country.",
        "continent": "dim_origin.continent.", "latitude": "dim_coffee.latitude.", "longitude": "dim_coffee.longitude.",
        "latitude_band": "dim_coffee.latitude_band.", "roast_level": "dim_roast.roast_level.",
        "roast_order": "dim_roast.roast_order.", "processing_method": "dim_process.processing_method.",
        "served_brew_method": "fact_coffee_rating.served_brew_method.", "brew_method": "dim_brew_method.method_name.",
        "acidity_level": "See fact_coffee_rating.", "body_level": "See fact_coffee_rating.",
        "sweetness_level": "See fact_coffee_rating.", "acidity_ord": "See fact_coffee_rating.",
        "body_ord": "See fact_coffee_rating.", "sweetness_ord": "See fact_coffee_rating.",
        "flavor_note_count": "See fact_coffee_rating.", "rating": "See fact_coffee_rating.",
        "rating_band": "See fact_coffee_rating.",
    },
}
TABLE_ORDER = ["dim_origin", "dim_roast", "dim_process", "dim_brew_method", "dim_coffee", "dim_flavor",
               "fact_coffee_rating", "bridge_coffee_flavor", "vw_coffee_flat"]
TABLE_NOTES = {
    "vw_coffee_flat": "View joining the fact and its single-valued dimensions; used by most analysis queries.",
    "bridge_coffee_flavor": "Many-to-many bridge between coffees and flavour notes.",
}


def _fmt(x) -> str:
    return f"{x:.4f}".rstrip("0").rstrip(".") if isinstance(x, float) else str(x)


def _allowed(con, table, col, ctype, is_key) -> str:
    n_distinct, n_rows = con.execute(f'SELECT COUNT(DISTINCT "{col}"), COUNT(*) FROM "{table}"').fetchone()
    if ctype == "TEXT":
        if n_distinct <= 12:
            return ", ".join(str(r[0]) for r in con.execute(f'SELECT DISTINCT "{col}" FROM "{table}" ORDER BY 1'))
        return "unique" if n_distinct == n_rows else f"{n_distinct} distinct values"
    if is_key:
        return "unique"
    lo, hi = con.execute(f'SELECT MIN("{col}"), MAX("{col}") FROM "{table}"').fetchone()
    return f"{_fmt(lo)} to {_fmt(hi)}"


def build(db_path: Path = DB_PATH) -> str:
    con = sqlite3.connect(db_path)
    lines = ["# Data Dictionary", "",
             "_Generated by `python -m pipeline.docgen` from `warehouse.db`; types come from the SQLite schema, "
             "examples and allowed values are observed in the data._", "",
             "Provenance, as far as the repo shows: `coffee_dataset.csv` (beans and ratings) has no documented source. "
             "The brewing-method attributes are hard-coded dictionaries in `notebooks/BREWING_METHODS_SCRAPING.ipynb` "
             "(comments cite USDA, Mayo Clinic and specialty coffee associations); the notebook also scrapes "
             "Wikipedia/Healthline snippets into a separate raw sheet. Nothing here was re-verified against those sources.", ""]
    for table in TABLE_ORDER:
        info = con.execute(f'PRAGMA table_info("{table}")').fetchall()  # cid,name,type,notnull,default,pk
        missing = [c[1] for c in info if c[1] not in DESCRIPTIONS[table]]
        if missing:
            raise KeyError(f"No description for {table}: {missing}")
        n = con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        lines += [f"## `{table}` ({n} rows)", ""]
        if table in TABLE_NOTES:
            lines += [TABLE_NOTES[table], ""]
        lines += ["| Column | Type | Key | Description | Example | Allowed / observed values |", "|---|---|---|---|---|---|"]
        fks = {r[3]: f"{r[2]}.{r[4]}" for r in con.execute(f'PRAGMA foreign_key_list("{table}")')}
        for _, name, ctype, _nn, _d, pk in info:
            key = "PK" if pk else ""
            if name in fks:
                key = (key + ", " if key else "") + f"FK -> {fks[name]}"
            example = con.execute(f'SELECT "{name}" FROM "{table}" LIMIT 1 OFFSET {n // 2}').fetchone()[0]
            lines.append(f"| `{name}` | {ctype or 'derived'} | {key} | {DESCRIPTIONS[table][name]} | "
                         f"`{example}` | {_allowed(con, table, name, ctype or 'TEXT', bool(pk))} |")
        lines.append("")
    con.close()
    return "\n".join(lines)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
