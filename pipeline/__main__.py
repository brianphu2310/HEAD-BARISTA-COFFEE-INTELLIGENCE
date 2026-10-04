"""Run the full pipeline: python -m pipeline"""
from pathlib import Path

from . import extract, load, transform, validate

ROOT = Path(__file__).resolve().parents[1]


def run(db_path: Path = load.DB_PATH, report_path: Path = ROOT / "docs" / "DATA_QUALITY.md") -> Path:
    beans = extract.extract_beans()
    methods = extract.extract_methods_xlsx()
    sql = extract.extract_sql()
    results = validate.run_checks(beans, methods, sql["mapping"], sql, extract.extract_beans(extract.BEANS_CSV_COPY))
    validate.write_report(results, report_path, {
        "coffee_dataset.csv": len(beans), "data/Coffee_Brewing_Dashboard_Final.xlsx": len(methods),
        "sql/Beans_And_Methods_Streamlit_Dataset.sql (method_mapping)": len(sql["mapping"])})
    validate.raise_on_errors(results)
    model = transform.build_model(beans, methods, sql["mapping"])
    out = load.load(model, db_path)
    print(f"Loaded {', '.join(f'{k}={len(v)}' for k, v in model.items())} -> {out.name}")
    return out


if __name__ == "__main__":
    run()
