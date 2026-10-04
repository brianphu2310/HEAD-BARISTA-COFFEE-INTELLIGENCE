"""Every analysis query runs, and key results are checked against independent pandas calculations."""
import importlib.util
from io import StringIO
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_queries", ROOT / "sql" / "run_queries.py")
run_queries = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_queries)
BEANS = pd.read_csv(ROOT / "coffee_dataset.csv")


@pytest.fixture(scope="module")
def results(warehouse, tmp_path_factory):
    return run_queries.run_all(warehouse, tmp_path_factory.mktemp("qr"))


def test_between_6_and_10_queries_all_return_rows(results):
    assert 6 <= len(results) <= 10
    assert all(len(df) > 0 for df in results.values())


def test_queries_use_required_techniques():
    text = "\n".join(p.read_text().upper() for p in (ROOT / "sql" / "analysis").glob("*.sql"))
    for token in ["WITH ", "RANK()", "LAG(", "PERCENT_RANK()", "NTILE(", "FIRST_VALUE(", "OVER (", "CASE", "JOIN"]:
        assert token in text, token


def test_origin_leaderboard_matches_pandas(results):
    r = results["01_origin_leaderboard"].set_index("origin")
    exp = BEANS.groupby("Origin")["Rating"].agg(["count", "mean", "max"])
    assert r["coffees"].sum() == 32 and len(r) == len(exp)
    for origin, row in exp.iterrows():
        assert r.loc[origin, "avg_rating"] == pytest.approx(row["mean"], abs=0.01)
        assert r.loc[origin, "best_rating"] == row["max"]
    assert r["rank_by_avg"].min() == 1


def test_top_per_method_is_at_most_two_and_sorted(results):
    r = results["02_top_coffees_per_method"]
    assert (r.groupby("brew_method").size() <= 2).all()
    first = r[r["rank_in_method"] == 1].set_index("brew_method")["rating"]
    second = r[r["rank_in_method"] == 2].set_index("brew_method")["rating"]
    assert (first.loc[second.index] >= second).all()


def test_roast_process_matrix_counts(results):
    assert results["03_roast_process_matrix"]["coffees"].sum() == 32


def test_distribution_percentiles(results):
    r = results["04_rating_distribution"]
    assert r["percent_rank"].between(0, 1).all() and r["cume_dist"].max() == 1.0
    assert set(r["quartile_1_is_top"]) == {1, 2, 3, 4}
    top = r.sort_values("rating", ascending=False).iloc[0]
    assert top["quartile_1_is_top"] == 1 and top["tier"] == "Top tier"


def test_flavour_lift_is_consistent(results):
    r = results["05_flavour_notes_lift"]
    assert (r["coffees"] >= 3).all()
    tokens = BEANS.assign(t=BEANS["Flavor_Notes"].str.split(",")).explode("t")
    tokens["t"] = tokens["t"].str.strip().str.lower()
    exp = tokens.groupby("t")["Rating"].agg(["count", "mean"])
    for _, row in r.iterrows():
        assert row["coffees"] == exp.loc[row["flavor_note"], "count"]
        assert row["avg_rating"] == pytest.approx(exp.loc[row["flavor_note"], "mean"], abs=0.01)


def test_method_ladder_keeps_methods_without_beans(results):
    r = results["06_method_caffeine_ladder"]
    assert len(r) == 13 and r["coffees_mapped"].sum() == 32
    assert (r[r["coffees_mapped"] == 0]["coverage_status"] == "No beans in dataset").all()
    assert pd.isna(r.iloc[0]["previous_faster_method"])
    assert r["running_coffees_mapped"].is_monotonic_increasing and r.iloc[-1]["running_coffees_mapped"] == 32


def test_latitude_band_pivot_adds_up(results):
    r = results["07_latitude_band_by_roast"].set_index("latitude_band")
    bands = r.drop(index="All coffees")
    assert bands["coffees"].sum() == r.loc["All coffees", "coffees"] == 32
    assert (bands[["light_roast", "medium_roast", "dark_roast"]].sum(axis=1) == bands["coffees"]).all()


def test_acidity_fit_percentages(results):
    r = results["08_acidity_fit_by_method"]
    assert r["coffees"].sum() == 32
    assert (r["matching_tier"] <= r["coffees"]).all() and r["pct_matching"].between(0, 100).all()


def test_best_coffee_per_origin(results):
    r = results["09_best_coffee_per_origin"].set_index("origin")
    assert len(r) == BEANS["Origin"].nunique()
    for origin, g in BEANS.groupby("Origin"):
        assert r.loc[origin, "best_rating"] == g["Rating"].max()
        assert r.loc[origin, "rating_spread"] == g["Rating"].max() - g["Rating"].min()
    assert r.loc["Panama", "best_coffee"] == "Panama Geisha"


def test_process_share_sums_to_100_per_continent(results):
    r = results["10_process_by_continent"]
    assert r.groupby("continent")["pct_of_continent"].sum().round(0).eq(100).all()


def test_committed_csv_outputs_are_current(results):
    for name, df in results.items():
        committed = pd.read_csv(ROOT / "docs" / "query_results" / f"{name}.csv")
        pd.testing.assert_frame_equal(committed, pd.read_csv(StringIO(df.to_csv(index=False))))
