"""Transform: normalise, derive features and build dimension/fact tables with surrogate keys."""
import pandas as pd

from .validate import ORIGIN_REF, caffeine_level, sleep_impact

ORD = {"Low": 1, "Medium": 2, "High": 3, "Light": 1, "Full": 3}  # ordinal encodings (analyst-defined)
ROAST_ORDER = {"Light": 1, "Medium": 2, "Dark": 3}


def rating_band(r: float) -> str:
    return "90+" if r >= 90 else "85-89" if r >= 85 else "Below 85"


def _keyed(values, col: str, key: str) -> pd.DataFrame:
    d = pd.DataFrame({col: sorted(set(values))})
    d.insert(0, key, range(1, len(d) + 1))
    return d


def build_model(beans: pd.DataFrame, methods: pd.DataFrame, mapping: pd.DataFrame) -> dict[str, pd.DataFrame]:
    b = beans.copy()
    for c in b.select_dtypes(include=["object", "string"]).columns:
        b[c] = b[c].astype(str).str.strip()
    b = b.drop_duplicates("Coffee_Name").sort_values("Coffee_Name").reset_index(drop=True)
    mp = mapping.drop_duplicates().set_index("coffee_method")["brewing_method"]  # exact duplicate row removed here

    dim_origin = _keyed(b["Origin"], "origin_country", "origin_key")
    dim_origin["continent"] = dim_origin["origin_country"].map(ORIGIN_REF)
    dim_roast = _keyed(b["Roast_Level"], "roast_level", "roast_key")
    dim_roast["roast_order"] = dim_roast["roast_level"].map(ROAST_ORDER)
    dim_roast = dim_roast.sort_values("roast_order").reset_index(drop=True)
    dim_roast["roast_key"] = range(1, len(dim_roast) + 1)
    dim_process = _keyed(b["Processing_Method"], "processing_method", "process_key")

    m = methods.copy().sort_values("Method").reset_index(drop=True)
    dim_brew_method = pd.DataFrame({
        "brew_method_key": range(1, len(m) + 1), "method_name": m["Method"],
        "brew_time_min": m["Brew_Time_min"].astype(float), "caffeine_mg": m["Caffeine_mg"].astype(int),
        "antioxidant_rank": m["Antioxidant_Rank"].astype(int), "acidity_score": m["Acidity"].astype(int),
        "bitterness_score": m["Bitterness"].astype(int), "body_score": m["Body"].astype(int),
        "complexity": m["Complexity"], "equipment": m["Equipment"], "quick_guide": m["Quick_Guide"],
        "primary_taste": m["Primary_Taste"],
        "caffeine_level": m["Caffeine_mg"].map(caffeine_level), "sleep_impact": m["Caffeine_mg"].map(sleep_impact),
        "score_index_excel": m["Score_Index"].astype(float)})

    dim_coffee = pd.DataFrame({"coffee_key": range(1, len(b) + 1), "coffee_name": b["Coffee_Name"],
                               "latitude": b["Latitude"], "longitude": b["Longitude"]})
    dim_coffee["latitude_band"] = b["Latitude"].abs().map(lambda v: "0-10" if v < 10 else "10-20" if v < 20 else "20+")

    tokens = b["Flavor_Notes"].str.split(",").map(lambda t: [x.strip().lower() for x in t if x.strip()])
    dim_flavor = _keyed({t for ts in tokens for t in ts}, "flavor_note", "flavor_key")
    fkey = dict(zip(dim_flavor["flavor_note"], dim_flavor["flavor_key"]))
    bridge = pd.DataFrame(sorted({(ck, fkey[t]) for ck, ts in zip(dim_coffee["coffee_key"], tokens) for t in ts}),
                          columns=["coffee_key", "flavor_key"])

    canon = b["Brew_Method"].map(mp)
    fact = pd.DataFrame({
        "coffee_key": dim_coffee["coffee_key"],
        "origin_key": b["Origin"].map(dict(zip(dim_origin["origin_country"], dim_origin["origin_key"]))),
        "roast_key": b["Roast_Level"].map(dict(zip(dim_roast["roast_level"], dim_roast["roast_key"]))),
        "process_key": b["Processing_Method"].map(dict(zip(dim_process["processing_method"], dim_process["process_key"]))),
        "brew_method_key": canon.map(dict(zip(dim_brew_method["method_name"], dim_brew_method["brew_method_key"]))),
        "served_brew_method": b["Brew_Method"],
        "acidity_level": b["Acidity"], "body_level": b["Body"], "sweetness_level": b["Sweetness"],
        "acidity_ord": b["Acidity"].map(ORD), "body_ord": b["Body"].map(ORD), "sweetness_ord": b["Sweetness"].map(ORD),
        "flavor_note_count": tokens.map(len), "rating": b["Rating"].astype(int),
        "rating_band": b["Rating"].map(rating_band)})
    return {"dim_origin": dim_origin, "dim_roast": dim_roast, "dim_process": dim_process,
            "dim_brew_method": dim_brew_method, "dim_coffee": dim_coffee, "dim_flavor": dim_flavor,
            "fact_coffee_rating": fact, "bridge_coffee_flavor": bridge}
