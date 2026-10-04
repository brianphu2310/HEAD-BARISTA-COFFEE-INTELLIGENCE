"""Tests for the extract -> validate -> transform -> load pipeline."""
import pandas as pd
import pytest

from pipeline import docgen, extract, transform, validate

ROOT = extract.ROOT


@pytest.fixture()
def src():
    sql = extract.extract_sql()
    return extract.extract_beans(), extract.extract_methods_xlsx(), sql["mapping"], sql


def _by_name(results):
    return {r.name: r for r in results}


def test_extract_shapes(src):
    beans, methods, mapping, sql = src
    assert beans.shape == (32, 12) and methods.shape == (13, 14)
    assert len(sql["beans"]) == 32 and len(sql["methods"]) == 13 and len(mapping) == 14


def test_source_passes_with_only_the_documented_warnings(src):
    beans, methods, mapping, sql = src
    results = validate.run_checks(beans, methods, mapping, sql, extract.extract_beans(extract.BEANS_CSV_COPY))
    assert len(results) >= 40
    assert not [r for r in results if r.status == "FAIL"]
    warned = {r.name for r in results if r.status == "WARN"}
    assert warned == {"Mapping: no exact duplicate rows", "Reconcile: `Score_Index` agrees between workbook and SQL"}


@pytest.mark.parametrize("mutate, check", [
    (lambda d: d.assign(Rating=d["Rating"].where(d.index != 0, 150)), "Beans: `Rating` within [0, 100]"),
    (lambda d: pd.concat([d, d.iloc[[0]]]), "Beans: unique `Coffee_Name`"),
    (lambda d: d.assign(Roast_Level=d["Roast_Level"].where(d.index != 0, "Burnt")),
     "Beans: `Roast_Level` in {Dark, Light, Medium}"),
    (lambda d: d.assign(Origin=d["Origin"].where(d.index != 0, "Narnia")), "Beans: `Origin` in origin reference"),
    (lambda d: d.assign(Brew_Method=d["Brew_Method"].where(d.index != 0, "Telepathy")),
     "Beans: `Brew_Method` has a canonical-method mapping"),
    (lambda d: d.assign(Flavor_Notes=d["Flavor_Notes"].where(d.index != 0, "floral,,citrus")),
     "Beans: `Flavor_Notes` has no empty tokens"),
    (lambda d: d.assign(Latitude=d["Latitude"].where(d.index != 0, 95.0)), "Beans: `Latitude` within [-90, 90]"),
])
def test_bean_checks_detect_injected_defects(src, mutate, check):
    beans, _, mapping, _ = src
    assert _by_name(validate.check_beans(mutate(beans.copy()), mapping))[check].status == "FAIL"


def test_null_bean_value_is_detected(src):
    beans, _, mapping, _ = src
    bad = beans.copy()
    bad.loc[3, "Rating"] = None
    assert _by_name(validate.check_beans(bad, mapping))["Beans: no nulls/blanks in `Rating`"].status == "FAIL"


def test_method_and_mapping_checks_detect_defects(src):
    _, methods, mapping, _ = src
    bad = methods.copy()
    bad.loc[0, "Acidity"] = 11
    assert _by_name(validate.check_methods(bad, mapping))["Methods: `Acidity` within [1, 10]"].status == "FAIL"
    conflicting = pd.concat([mapping, pd.DataFrame([{"coffee_method": "Chemex", "brewing_method": "Espresso"}])])
    assert _by_name(validate.check_methods(methods, conflicting))[
        "Mapping: no conflicting targets for a bean method"].status == "FAIL"
    orphan = pd.concat([mapping, pd.DataFrame([{"coffee_method": "X", "brewing_method": "Nope"}])])
    assert _by_name(validate.check_methods(methods, orphan))[
        "Mapping: every target exists in the methods table"].status == "FAIL"


def test_reconciliation_detects_drift(src):
    beans, methods, mapping, sql = src
    drift = beans.copy()
    drift.loc[0, "Rating"] += 1
    res = _by_name(validate.check_reconciliation(drift, methods, sql))
    assert res["Reconcile: coffee_dataset.csv equals `coffee_data` CTE in SQL script"].status == "FAIL"


def test_errors_block_the_load(src):
    beans, methods, mapping, sql = src
    with pytest.raises(validate.DataQualityError):
        validate.raise_on_errors(validate.run_checks(beans.drop(columns=["Rating"]), methods, mapping))


def test_caffeine_rules_match_workbook_labels(src):
    _, methods, _, _ = src
    assert (methods["Caffeine_mg"].map(validate.caffeine_level) == methods["Caffeine_Level"]).all()
    assert validate.caffeine_level(75) == "Low" and validate.caffeine_level(150) == "Medium"
    assert validate.sleep_impact(200) == "May affect sleep" and validate.sleep_impact(201) == "Avoid after 2 PM"


def test_transform_model(src):
    beans, methods, mapping, _ = src
    m = transform.build_model(beans, methods, mapping)
    assert len(m["fact_coffee_rating"]) == 32 and len(m["dim_brew_method"]) == 13
    assert len(m["dim_flavor"]) == 25
    assert m["fact_coffee_rating"].notna().all().all()
    assert m["bridge_coffee_flavor"].duplicated().sum() == 0
    flat = m["fact_coffee_rating"].merge(m["dim_coffee"], on="coffee_key").set_index("coffee_name")
    assert flat.loc["Panama Geisha", "rating_band"] == "90+" and flat.loc["Kenya Peaberry", "rating_band"] == "90+"
    assert flat.loc["Brazil Santos", "rating_band"] == "Below 85"
    assert flat.loc["Ethiopia Yirgacheffe", "flavor_note_count"] == 3
    # Chemex / Clever Dripper / Nel Drip all collapse to Pour Over
    pour = m["dim_brew_method"].set_index("method_name").loc["Pour Over", "brew_method_key"]
    assert flat.loc["Kenya Peaberry", "brew_method_key"] == pour and flat.loc["Kenya Peaberry", "served_brew_method"] == "Chemex"


def test_transform_is_deterministic(src):
    beans, methods, mapping, _ = src
    a = transform.build_model(beans, methods, mapping)
    b = transform.build_model(beans.sample(frac=1, random_state=3), methods, mapping)
    for name in a:
        pd.testing.assert_frame_equal(a[name].reset_index(drop=True), b[name].reset_index(drop=True))


def test_rating_band_boundaries():
    assert [transform.rating_band(x) for x in (90, 89, 85, 84)] == ["90+", "85-89", "85-89", "Below 85"]


def test_load_counts_fk_and_constraints(con):
    n = lambda t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]  # noqa: E731
    assert (n("dim_origin"), n("dim_roast"), n("dim_process"), n("dim_brew_method"), n("dim_coffee"),
            n("dim_flavor"), n("fact_coffee_rating"), n("bridge_coffee_flavor")) == (21, 3, 5, 13, 32, 25, 32, 73)
    assert con.execute("PRAGMA foreign_key_check").fetchall() == []
    with pytest.raises(Exception):
        con.execute("INSERT INTO bridge_coffee_flavor VALUES (999, 999)")
    with pytest.raises(Exception):  # CHECK constraint
        con.execute("UPDATE fact_coffee_rating SET rating = 500 WHERE coffee_key = 1")


def test_indexes_exist(con):
    names = {r[1] for r in con.execute("SELECT * FROM sqlite_master WHERE type='index'")}
    assert {"ix_fact_origin", "ix_fact_method", "ix_fact_rating", "ix_bridge_flavor"} <= names


def test_committed_docs_are_current(warehouse):
    assert docgen.build(warehouse) == (ROOT / "docs" / "DATA_DICTIONARY.md").read_text(encoding="utf-8")
    assert (warehouse.parent / "DATA_QUALITY.md").read_text(encoding="utf-8") == \
        (ROOT / "docs" / "DATA_QUALITY.md").read_text(encoding="utf-8")


def test_every_warehouse_column_is_documented(con):
    for table, cols in docgen.DESCRIPTIONS.items():
        assert sorted(r[1] for r in con.execute(f"PRAGMA table_info({table})")) == sorted(cols)


def test_mermaid_diagram_mentions_every_table():
    text = (ROOT / "docs" / "DATA_MODEL.md").read_text(encoding="utf-8")
    assert "```mermaid" in text and "erDiagram" in text
    for t in ["dim_origin", "dim_roast", "dim_process", "dim_brew_method", "dim_coffee", "dim_flavor",
              "fact_coffee_rating", "bridge_coffee_flavor"]:
        assert t in text
