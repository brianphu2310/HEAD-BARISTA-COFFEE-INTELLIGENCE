"""Validate: data-quality checks run before anything is loaded.

ERROR failures stop the load; WARN failures are reported only (known source quirks end up here).
"""
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

BEAN_REQUIRED = ["Coffee_Name", "Origin", "Latitude", "Longitude", "Roast_Level", "Processing_Method",
                 "Brew_Method", "Acidity", "Body", "Sweetness", "Flavor_Notes", "Rating"]
DOMAINS = {  # categorical columns of the beans table
    "Roast_Level": {"Light", "Medium", "Dark"},
    "Acidity": {"Low", "Medium", "High"},
    "Body": {"Light", "Medium", "Full"},
    "Sweetness": {"Low", "Medium", "High"},
    "Processing_Method": {"Washed", "Natural", "Honey", "Wet Hulled", "Monsooned"},
}
# Analyst-defined reference table (not in the source data): origin -> continent grouping.
ORIGIN_REF = {
    "Ethiopia": "Africa", "Kenya": "Africa", "Tanzania": "Africa", "Rwanda": "Africa", "Uganda": "Africa",
    "Colombia": "South America", "Brazil": "South America", "Peru": "South America", "Bolivia": "South America",
    "Costa Rica": "North America", "Guatemala": "North America", "Mexico": "North America",
    "Jamaica": "North America", "USA": "North America", "Panama": "North America",
    "Indonesia": "Asia", "Vietnam": "Asia", "India": "Asia", "Thailand": "Asia", "Myanmar": "Asia",
    "Papua New Guinea": "Oceania",
}
METHOD_SCALES = ["Acidity", "Bitterness", "Body"]  # 1-10
COMPLEXITY = {"Low", "Medium", "High"}


class DataQualityError(RuntimeError):
    pass


@dataclass
class CheckResult:
    name: str
    category: str
    passed: bool
    detail: str
    severity: str = "ERROR"

    @property
    def status(self) -> str:
        return "PASS" if self.passed else ("FAIL" if self.severity == "ERROR" else "WARN")


def _res(name, category, bad, ok_detail, severity="ERROR"):
    detail = ok_detail if not bad else f"{len(bad)} issue(s): " + "; ".join(map(str, bad[:5]))
    return CheckResult(name, category, not bad, detail, severity)


def caffeine_level(mg: float) -> str:
    """Rule taken from the CASE expression in sql/Beans_And_Methods_Streamlit_Dataset.sql."""
    return "Low" if mg <= 75 else "Medium" if mg <= 150 else "High"


def sleep_impact(mg: float) -> str:
    return "Won't disrupt sleep" if mg <= 75 else "May affect sleep" if mg <= 200 else "Avoid after 2 PM"


def check_beans(beans: pd.DataFrame, mapping: pd.DataFrame) -> list[CheckResult]:
    r: list[CheckResult] = []
    missing = [c for c in BEAN_REQUIRED if c not in beans.columns]
    r.append(_res("Beans: required columns present", "schema", missing, f"{len(BEAN_REQUIRED)} columns found"))
    if missing:
        return r
    r.append(_res("Beans: table is not empty", "schema", [] if len(beans) else ["0 rows"], f"{len(beans)} rows"))
    for c in BEAN_REQUIRED:
        n = int(beans[c].isna().sum() + (beans[c].astype(str).str.strip() == "").sum())
        r.append(_res(f"Beans: no nulls/blanks in `{c}`", "completeness", [f"{n} null/blank"] if n else [], "0 nulls"))
    d = beans[beans.duplicated("Coffee_Name", keep=False)]
    r.append(_res("Beans: unique `Coffee_Name`", "uniqueness", sorted(d["Coffee_Name"].unique()), "no duplicates"))
    d = beans[beans.duplicated(keep=False)]
    r.append(_res("Beans: no fully duplicated rows", "uniqueness", sorted(d["Coffee_Name"].unique()), "no duplicates"))
    for col, lo, hi in [("Rating", 0, 100), ("Latitude", -90, 90), ("Longitude", -180, 180)]:
        v = pd.to_numeric(beans[col], errors="coerce")
        r.append(_res(f"Beans: `{col}` within [{lo}, {hi}]", "range", beans.loc[~v.between(lo, hi), "Coffee_Name"].tolist(),
                      f"observed {v.min():g} to {v.max():g}"))
    for col, allowed in DOMAINS.items():
        bad = beans.loc[~beans[col].isin(allowed), col].unique().tolist()
        r.append(_res(f"Beans: `{col}` in {{{', '.join(sorted(allowed))}}}", "domain", bad, "all values allowed"))
    notes = beans["Flavor_Notes"].astype(str).str.split(",")
    bad = beans.loc[notes.map(lambda t: any(x.strip() == "" for x in t)), "Coffee_Name"].tolist()
    r.append(_res("Beans: `Flavor_Notes` has no empty tokens", "domain", bad, "all lists well-formed"))
    r.append(_res("Beans: `Origin` in origin reference", "referential",
                  sorted(set(beans["Origin"]) - set(ORIGIN_REF)), f"{beans['Origin'].nunique()} origins known"))
    r.append(_res("Beans: `Brew_Method` has a canonical-method mapping", "referential",
                  sorted(set(beans["Brew_Method"]) - set(mapping["coffee_method"])),
                  f"{beans['Brew_Method'].nunique()} labels mapped"))
    z = (beans["Rating"] - beans["Rating"].mean()) / beans["Rating"].std()
    r.append(_res("Beans: rating outliers (|z| > 3)", "outlier", beans.loc[z.abs() > 3, "Coffee_Name"].tolist(),
                  "none", severity="WARN"))
    return r


def check_methods(methods: pd.DataFrame, mapping: pd.DataFrame) -> list[CheckResult]:
    r: list[CheckResult] = []
    r.append(_res("Methods: unique `Method`", "uniqueness", methods.loc[methods["Method"].duplicated(), "Method"].tolist(),
                  f"{len(methods)} methods"))
    r.append(_res("Methods: no nulls in numeric/label columns", "completeness",
                  [c for c in methods.columns if methods[c].isna().any()], "0 nulls"))
    for c in METHOD_SCALES:
        v = methods[c]
        r.append(_res(f"Methods: `{c}` within [1, 10]", "range", methods.loc[~v.between(1, 10), "Method"].tolist(),
                      f"observed {v.min():g} to {v.max():g}"))
    r.append(_res("Methods: `Antioxidant_Rank` within [1, 5]", "range",
                  methods.loc[~methods["Antioxidant_Rank"].between(1, 5), "Method"].tolist(), "all within range"))
    r.append(_res("Methods: `Brew_Time_min` and `Caffeine_mg` positive", "range",
                  methods.loc[(methods["Brew_Time_min"] <= 0) | (methods["Caffeine_mg"] <= 0), "Method"].tolist(),
                  f"brew time {methods['Brew_Time_min'].min():g} to {methods['Brew_Time_min'].max():g} min"))
    r.append(_res("Methods: `Complexity` in {Low, Medium, High}", "domain",
                  methods.loc[~methods["Complexity"].isin(COMPLEXITY), "Method"].tolist(), "all values allowed"))
    if "Caffeine_Level" in methods and "Sleep_Impact" in methods:
        bad = methods.loc[(methods["Caffeine_Level"] != methods["Caffeine_mg"].map(caffeine_level))
                          | (methods["Sleep_Impact"] != methods["Caffeine_mg"].map(sleep_impact)), "Method"].tolist()
        r.append(_res("Methods: workbook caffeine/sleep labels follow the SQL CASE rules", "consistency", bad,
                      "labels reproducible from `Caffeine_mg`"))
    # mapping table
    dup = mapping[mapping.duplicated(keep="first")]
    conflict = mapping.groupby("coffee_method")["brewing_method"].nunique()
    r.append(_res("Mapping: no conflicting targets for a bean method", "uniqueness", conflict[conflict > 1].index.tolist(),
                  "one target per label"))
    r.append(_res("Mapping: no exact duplicate rows", "uniqueness", dup["coffee_method"].tolist(),
                  "no duplicates", severity="WARN"))
    r.append(_res("Mapping: every target exists in the methods table", "referential",
                  sorted(set(mapping["brewing_method"]) - set(methods["Method"])), "all targets found"))
    return r


def check_reconciliation(beans, methods_x, sql: dict, csv_copy: pd.DataFrame | None = None) -> list[CheckResult]:
    r: list[CheckResult] = []
    key = "Coffee_Name"
    a = beans.sort_values(key).reset_index(drop=True)
    b = sql["beans"].sort_values(key).reset_index(drop=True)[list(beans.columns)]
    r.append(CheckResult("Reconcile: coffee_dataset.csv equals `coffee_data` CTE in SQL script", "reconciliation",
                         a.round(4).equals(b.round(4)), f"{len(a)} CSV rows vs {len(b)} SQL rows"))
    if csv_copy is not None:
        r.append(CheckResult("Reconcile: sql/coffee_dataset.csv is an exact copy of coffee_dataset.csv", "reconciliation",
                             csv_copy.equals(beans), "identical copies", severity="WARN"))
    mx = methods_x.set_index("Method")
    ms = sql["methods"].set_index("Method").reindex(mx.index)
    shared = ["Brew_Time_min", "Caffeine_mg", "Antioxidant_Rank", "Acidity", "Bitterness", "Body"]
    diff = [c for c in shared if not (mx[c].astype(float) == ms[c]).all()]
    r.append(_res("Reconcile: workbook methods equal `brewing_methods` CTE (shared columns)", "reconciliation", diff,
                  f"{len(shared)} shared columns identical for {len(mx)} methods"))
    n_diff = int((mx["Score_Index"].astype(float) != ms["Score_Index"]).sum())
    wb, sq = mx["Score_Index"].astype(float), ms["Score_Index"]
    r.append(CheckResult("Reconcile: `Score_Index` agrees between workbook and SQL", "reconciliation", n_diff == 0,
                         "identical" if n_diff == 0 else
                         f"{n_diff} of {len(mx)} methods differ (workbook {wb.min():g}-{wb.max():g}, SQL {sq.min():g}-"
                         f"{sq.max():g}); the formula is not documented, so the pipeline keeps the workbook value as "
                         "`score_index_excel` and does not use it", severity="WARN"))
    return r


def run_checks(beans, methods, mapping, sql=None, csv_copy=None) -> list[CheckResult]:
    results = check_beans(beans, mapping) + check_methods(methods, mapping)
    if sql is not None:
        results += check_reconciliation(beans, methods, sql, csv_copy)
    return results


def raise_on_errors(results: list[CheckResult]) -> None:
    failed = [r for r in results if r.status == "FAIL"]
    if failed:
        raise DataQualityError("; ".join(f"{r.name}: {r.detail}" for r in failed))


def write_report(results: list[CheckResult], path: Path, sources: dict[str, int]) -> None:
    c = {s: sum(r.status == s for r in results) for s in ("PASS", "WARN", "FAIL")}
    lines = ["# Data Quality Report", "",
             "_Generated by `python -m pipeline` (`pipeline/validate.py`). Re-run to refresh._", "",
             "Sources: " + ", ".join(f"`{k}` ({v} rows)" for k, v in sources.items()),
             f"- Checks: {len(results)} total, **{c['PASS']} passed**, {c['WARN']} warnings, {c['FAIL']} failures", "",
             "| Status | Category | Check | Detail |", "|---|---|---|---|"]
    lines += [f"| {r.status} | {r.category} | {r.name} | {r.detail} |" for r in results]
    lines += ["", "ERROR-severity failures stop the load into the warehouse; WARN items are known source quirks or "
              "informational. Warnings are not hidden: they describe how the repo's own files disagree.", ""]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines), encoding="utf-8")
