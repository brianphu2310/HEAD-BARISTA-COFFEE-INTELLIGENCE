"""Extract the three sources the repo already contains.

1. coffee_dataset.csv                          - 32 coffee beans (provenance not documented in the repo)
2. data/Coffee_Brewing_Dashboard_Final.xlsx    - 13 brewing methods (master sheet built by the scraping notebook)
3. sql/Beans_And_Methods_Streamlit_Dataset.sql - CTEs holding the same beans, the same methods and the
                                                 bean-brew-method -> canonical-method mapping

The SQL file is parsed so the three sources can be reconciled and so the mapping has a single origin.
"""
import re
import warnings
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BEANS_CSV = ROOT / "coffee_dataset.csv"
BEANS_CSV_COPY = ROOT / "sql" / "coffee_dataset.csv"
METHODS_XLSX = ROOT / "data" / "Coffee_Brewing_Dashboard_Final.xlsx"
STREAMLIT_SQL = ROOT / "sql" / "Beans_And_Methods_Streamlit_Dataset.sql"

BEAN_COLUMNS = ["Coffee_Name", "Origin", "Latitude", "Longitude", "Roast_Level", "Processing_Method",
                "Brew_Method", "Acidity", "Body", "Sweetness", "Flavor_Notes", "Rating"]
METHOD_COLUMNS = ["Method", "Brew_Time_min", "Caffeine_mg", "Antioxidant_Rank", "Acidity", "Bitterness",
                  "Body", "Complexity", "Equipment", "Quick_Guide", "Primary_Taste", "Caffeine_Level",
                  "Sleep_Impact", "Score_Index"]
XLSX_HEADER = ["Method", "Brew Time (min)", "Caffeine (mg)", "Antioxidant Rank (1-5)", "Acidity (1-10)",
               "Bitterness (1-10)", "Body (1-10)", "Complexity", "Recommended Equipment",
               "Quick Brewing Guide", "Primary Taste", "Caffeine Level", "Sleep Impact", "Score Index"]


def extract_beans(path: Path = BEANS_CSV) -> pd.DataFrame:
    return pd.read_csv(path)


def extract_methods_xlsx(path: Path = METHODS_XLSX) -> pd.DataFrame:
    """Read the first sheet of the dashboard workbook: a title block, then a header row, then one row per method."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # openpyxl warns about Excel conditional-format extensions
        raw = pd.read_excel(path, sheet_name=0, header=None)
    start = raw.index[raw.iloc[:, 0] == "Method"][0]
    header = raw.iloc[start].tolist()
    if header != XLSX_HEADER:
        raise ValueError(f"Unexpected workbook header: {header}")
    body = raw.iloc[start + 1:]
    stop = body.iloc[:, 1].isna().to_numpy().argmax() if body.iloc[:, 1].isna().any() else len(body)
    df = body.iloc[:stop].copy()
    df.columns = METHOD_COLUMNS
    for col in ["Brew_Time_min", "Caffeine_mg", "Antioxidant_Rank", "Acidity", "Bitterness", "Body", "Score_Index"]:
        df[col] = pd.to_numeric(df[col])
    # the workbook stores caffeine levels with an emoji prefix; keep the text label only
    df["Caffeine_Level"] = df["Caffeine_Level"].astype(str).str.replace(r"^[^A-Za-z]+", "", regex=True)
    return df.reset_index(drop=True)


def _cte_block(sql: str, name: str) -> str:
    m = re.search(rf"{name}\s+AS\s*\((.*?)\n\)", sql, flags=re.S)
    if not m:
        raise ValueError(f"CTE {name} not found in {STREAMLIT_SQL.name}")
    return re.sub(r"\s+AS\s+[A-Za-z_]+", "", m.group(1))  # drop column aliases of the first SELECT


def extract_sql(path: Path = STREAMLIT_SQL) -> dict[str, pd.DataFrame]:
    """Parse the coffee_data, brewing_methods and method_mapping CTEs of the Streamlit SQL script."""
    sql = Path(path).read_text(encoding="utf-8")
    q, n = r"'([^']*)'", r"(-?[\d.]+)"
    beans = re.findall(rf"SELECT {q},\s*{q},\s*{n},\s*{n},\s*{q},\s*{q},\s*{q},\s*{q},\s*{q},\s*{q},\s*{q},\s*(\d+)",
                       _cte_block(sql, "coffee_data"))
    methods = re.findall(rf"SELECT {q},\s*{n},\s*{n},\s*{n},\s*{n},\s*{n},\s*{n},\s*{q},\s*{n}",
                         _cte_block(sql, "brewing_methods"))
    mapping = re.findall(rf"SELECT {q},\s*{q}", _cte_block(sql, "method_mapping"))
    b = pd.DataFrame(beans, columns=BEAN_COLUMNS)
    b[["Latitude", "Longitude"]] = b[["Latitude", "Longitude"]].astype(float)
    b["Rating"] = b["Rating"].astype(int)
    m = pd.DataFrame(methods, columns=["Method", "Brew_Time_min", "Caffeine_mg", "Antioxidant_Rank", "Acidity",
                                       "Bitterness", "Body", "Complexity", "Score_Index"])
    m[[c for c in m.columns if c not in ("Method", "Complexity")]] = \
        m[[c for c in m.columns if c not in ("Method", "Complexity")]].astype(float)
    return {"beans": b, "methods": m,
            "mapping": pd.DataFrame(mapping, columns=["coffee_method", "brewing_method"])}
