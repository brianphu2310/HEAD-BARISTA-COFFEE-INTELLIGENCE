<img width="594" height="670" alt="image" src="https://github.com/user-attachments/assets/d572b47b-0d56-4600-8b2a-b8802460865e" />


# ☕ Head Barista Coffee Intelligence
### *An end-to-end data project that started with one obsessive question about extraction ratios — and ended with a deployed brewing consultant*

[![Streamlit App](https://img.shields.io/badge/☕_Streamlit_App-Live-00C7A3?style=for-the-badge&logo=streamlit&logoColor=white)](https://testing-wzx24gsioxffy3mkvtvnsj.streamlit.app)
[![Tableau](https://img.shields.io/badge/📊_Tableau_Dashboard-Live-9B59EF?style=for-the-badge&logo=tableau&logoColor=white)](https://public.tableau.com/app/profile/brian.ma5935/viz/Cofffee_Brian_Project/Dashboard3)
[![Colab](https://img.shields.io/badge/📓_Full_Analysis-Google_Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com/drive/1uCOkUri0_LfMO2CzFqoj9uhfkYfHehvo)
[![Kaggle Dataset](https://img.shields.io/badge/📦_Dataset-Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/brianphu)
[![License: MIT](https://img.shields.io/badge/License-MIT-gray?style=for-the-badge)](LICENSE)

---

## At a glance

[![CI](https://github.com/brianphu2310/HEAD-BARISTA-COFFEE-INTELLIGENCE/actions/workflows/ci.yml/badge.svg)](https://github.com/brianphu2310/HEAD-BARISTA-COFFEE-INTELLIGENCE/actions)

| | |
|---|---|
| **Question** | Which brewing method and bean suit which customer, and can public data back a recommender? |
| **What I built** | Scraped and curated brewing dataset in SQL, statistical analysis, a Streamlit bean consultant, Tableau and Power BI dashboards. |
| **Key results** | Acidity and body are strongly inversely correlated across methods (-0.71). Ethiopian beans suit 7 of 8 methods. AeroPress is the most forgiving route to complex flavour. |
| **Proof** | CI green, 59 tests; a manual live-ingestion run is recorded in [docs/LIVE_RUN.md](docs/LIVE_RUN.md): Wikipedia 13 rows, Healthline 3, NCA 5 headings. |
| **Honest limits** | Perfect Daily Grind returned a bot challenge, so it is logged as 0 rows and not bypassed. Sensory scores are curated values, not scraped. Findings rest on a small method-level dataset. |

## The Problem I Was Actually Trying to Solve

I used to work as a barista — pulling shots, steaming milk, dialling in grinders. It was repetitive in the best possible way. Every morning the same ritual, but every cup slightly different depending on humidity, grind size, tamp pressure, bean origin.

What drove me insane was customer questions I couldn't answer well.

*"What's the difference between a Chemex and a V60?"*
*"If I like strong coffee, which beans should I get?"*
*"Is Ethiopian better than Colombian for espresso?"*

I knew the *vibe* of the answers from experience. But I didn't have **data** behind them. I was giving recommendations the same way every barista does — based on personal preference dressed up as expertise.

That bothered me more and more. The coffee world is full of strong opinions and very little analysis.

> *If you scraped every brewing method, mapped the flavour profiles, cross-referenced bean origins, and built a model on top — could you give a customer a genuinely data-driven recommendation in 30 seconds?*

I left the counter, opened a laptop, and built this.

---

##  What This Project Solves

### Problem 1: Customers don't know which brewing method suits them

| Before | After |
|--------|-------|
| "Just try an espresso" — generic advice based on nothing | App asks **4 questions** and recommends the best brewing method for you |
| No data on how methods differ by strength, acidity, body | **Structured comparison** across 8+ brewing methods |
| Barista recommendations are subjective and inconsistent | **Consistent, data-backed** consultant available 24/7 |

**Solution:** Streamlit app (Coffee Beans Consultant) — takes your flavour preferences and recommends the optimal method.

---

### Problem 2: No structured dataset exists for brewing method comparison

| Before | After |
|--------|-------|
| Brewing method info is scattered across blogs, forums, manufacturer sites | **Single structured dataset** scraped and cleaned from multiple sources |
| No standardised metrics for comparing methods | Consistent attributes: brew time, water temp, grind size, strength, acidity, body |
| Hobbyists rely on YouTube and Reddit for guidance | **Excel dashboard** with pivot tables for side-by-side comparison |

**Solution:** `BREWING_METHODS_SCRAPING.ipynb` — multi-source scraping pipeline → `Coffee_Brewing_Methods_Raw.xlsx` → `Coffee_Brewing_Dashboard_Final.xlsx`.

---

### Problem 3: Business owners don't know what to stock or promote

| Before | After |
|--------|-------|
| Café owners guess which beans and methods are trending | **Tableau dashboard** shows popularity patterns and flavour distribution |
| No visual way to compare brewing methods at scale | **Interactive filters** by brew style, strength, acidity, origin |
| "What should I put on the menu?" answered by gut feel | **Data-driven menu decisions** backed by structured analysis |

**Solution:** Tableau dashboard with filters for brew method, roast level, bean origin, and flavour profile.

---

### Problem 4: The "perfect cup" question has no consistent answer

| Before | After |
|--------|-------|
| "Best brewing method" varies by who you ask | **Flavour matrix** maps each method across 5 taste dimensions |
| No data on how bean origin interacts with brewing method | **Cross-analysis** of origin × method shows which combinations score highest |
| Beginners overwhelmed by options | **Tiered recommendations:** beginner / intermediate / enthusiast |

**Solution:** Colab analysis — correlation between brewing parameters and flavour outcome, visualised with Plotly.

---

##  Live Demos
<img width="1373" height="584" alt="Screenshot 2026-04-16 at 8 24 48 pm" src="https://github.com/user-attachments/assets/3858badb-d28a-43d8-8b37-eae51030b90f" />


### 1 — Tableau Dashboard · Brewing Intelligence Report

>  **[View Dashboard →](https://public.tableau.com/app/profile/brian.ma5935/viz/Cofffee_Brian_Project/Dashboard3)**
<img width="1279" height="752" alt="Pasted Graphic 1" src="https://github.com/user-attachments/assets/08714b18-642e-45c0-b206-00d52fc2b476" />


**What you can do:**
- Filter brewing methods by strength, acidity, body, and brew time
- Compare bean origins side by side
- Identify which methods dominate which flavour profiles
- Spot trends across roast levels (Light / Medium / Dark)

---

### 1b — Power BI Dashboard · Barista's Brewing Handbook

The same brewing data rebuilt in Power BI (the Tableau dashboard above is kept). Pick your situation with the dropdowns (time available, taste, acidity, health focus, sleep impact) and every page filters together. A one-line summary at the top says what the selection means, for example "13 methods | best overall: Cold Drip".

| Page | What it answers |
|---|---|
| Summary | Which method scores best overall, antioxidants vs caffeine by taste |
| How to brew | Time, caffeine, equipment and a quick guide for each method |
| Equipments | Brew time and complexity by method, equipment needed |
| Advices | Caffeine per cup, coloured by sleep impact |
| Beans | 32 beans by origin and roast, origin map, rating by roast |
| About | Definitions, source and limits |

<img src="docs/powerbi/barista-1.png" alt="Power BI summary page" width="900" />

- File: [`powerbi/barista_dashboard.pbix`](powerbi/barista_dashboard.pbix). All six pages: [`docs/powerbi/`](docs/powerbi/).
- Model: star schema (`fact_coffee_rating`, `dim_brew_method`, `dim_coffee`, `dim_origin`, `dim_roast`, `dim_process`, `dim_flavor`, `bridge_coffee_flavor`) (`bridge_coffee_flavor` links beans to flavours).
- Limits: antioxidant rank and taste scores are the repo workbook's relative scores, not lab measurements. The time / acidity / health-focus buckets are analyst rules derived from those scores, not medical advice. The origin map is bubbles at average bean coordinates, not a true basemap. The source of the 32-bean rows is not documented in the repo.

---

### 2 — Streamlit App · Coffee Beans Consultant

>  **[Launch App →](https://testing-wzx24gsioxffy3mkvtvnsj.streamlit.app)**

<img width="1512" height="842" alt="image" src="https://github.com/user-attachments/assets/930ad19b-c087-4e80-b992-b367283b63ac" />


**How the consultant works:**
1. Tell the app how strong you like your coffee
2. Select your preferred flavour notes (fruity / nutty / chocolatey / floral)
3. Pick your experience level (beginner / home enthusiast / advanced)
4. Get your **personalised brewing method recommendation** with bean pairing

**What you get:**
- Top recommended brewing method with explanation
- Alternative methods ranked by fit
- Bean origin recommendations matched to your flavour preference
- Brewing parameters: grind size, water temp, brew time, ratio

---

### 3 — Google Colab · Full Analysis

>  **[Open in Colab →](https://colab.research.google.com/drive/1uCOkUri0_LfMO2CzFqoj9uhfkYfHehvo)**

![Colab Analysis](https://github.com/user-attachments/assets/f9991756-ebb2-4eaf-a4e0-057cb7ba4d02)
<img width="1509" height="852" alt="image" src="https://github.com/user-attachments/assets/e5465a9a-1bc1-4bf4-b74e-2475213ff550" />
<img width="697" height="342" alt="image" src="https://github.com/user-attachments/assets/c0d21bcb-14bd-4dd4-9e37-a84e6773f93d" />
<img width="1505" height="851" alt="image" src="https://github.com/user-attachments/assets/b5f721d6-915c-4116-9c2e-379afea49b0f" />

**What's in the notebook:**
- Full EDA on brewing methods dataset
- Flavour profile clustering (which methods taste similar?)
- Bean origin × brewing method cross-analysis
- Distribution plots: brew time, water temperature, strength scores
- Correlation heatmap: which parameters actually drive flavour outcome?

Click **Runtime → Run all** to reproduce every chart.

---

##  Data Collection — Brewing Methods Scraping

**File:** `BREWING_METHODS_SCRAPING.ipynb`

No paid APIs. No synthetic data. Every data point scraped from publicly available coffee knowledge bases, manufacturer guides, and specialty coffee communities.

### What was scraped

| Attribute | Description | Example |
|-----------|-------------|---------|
| `method_name` | Name of brewing method | V60, Chemex, Aeropress, Espresso |
| `brew_time_min` | Brew time in minutes | 3.5 |
| `water_temp_c` | Optimal water temperature (°C) | 93 |
| `grind_size` | Coarseness level | Medium-Fine |
| `strength_score` | Strength rating 1–10 | 8 |
| `acidity_score` | Acidity rating 1–10 | 7 |
| `body_score` | Body/mouthfeel rating 1–10 | 5 |
| `difficulty` | Skill required | Beginner / Intermediate / Advanced |
| `recommended_roast` | Best roast type for this method | Light, Medium |
| `bean_origins` | Compatible origins | Ethiopia, Colombia, Kenya |
| `flavour_notes` | Primary flavour descriptors | Fruity, Floral, Bright |

### Scraping pipeline

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

SOURCES = [
    "https://perfectdailygrind.com/brewing-methods",
    "https://www.homegrounds.co/types-of-coffee",
    "https://www.javapresse.com/brewing-methods",
]

brewing_methods = []

for source_url in SOURCES:
    response = requests.get(source_url, headers=HEADERS)
    soup     = BeautifulSoup(response.content, 'html.parser')

    # Extract method cards/sections
    method_cards = soup.select('.method-card, .brewing-section, article.post')

    for card in method_cards:
        method = {
            'method_name':      extract_text(card, '.method-title, h2, h3'),
            'brew_time':        extract_text(card, '.brew-time, [data-brew-time]'),
            'water_temp':       extract_text(card, '.water-temp, [data-temp]'),
            'grind_size':       extract_text(card, '.grind-size, [data-grind]'),
            'difficulty':       extract_text(card, '.difficulty, .skill-level'),
            'flavour_notes':    extract_list(card, '.flavour-notes li, .taste-notes li'),
            'bean_origins':     extract_list(card, '.origins li, .bean-origins li'),
        }
        brewing_methods.append(method)

    time.sleep(1.5)  # polite crawl delay

df_raw = pd.DataFrame(brewing_methods)
df_raw.to_excel('Coffee_Brewing_Methods_Raw.xlsx', index=False)
print(f"Scraped: {len(df_raw)} brewing method records")
```

### Standardisation & cleaning

```python
# Strength, acidity, body were text descriptions — convert to numeric scores
strength_map = {
    'very mild': 2, 'mild': 3, 'medium': 5,
    'strong': 7, 'very strong': 9, 'intense': 10
}
acidity_map = {
    'low': 2, 'medium-low': 4, 'medium': 5,
    'medium-high': 7, 'high': 8, 'very high': 10
}

df['strength_score'] = df['strength'].str.lower().map(strength_map)
df['acidity_score']  = df['acidity'].str.lower().map(acidity_map)

# Brew time: "3-4 minutes" → take midpoint
df['brew_time_min'] = df['brew_time'].apply(
    lambda x: sum(map(float, re.findall(r'\d+\.?\d*', str(x)))) / 
              len(re.findall(r'\d+\.?\d*', str(x))) if x else None
)

# Water temp: "90-96°C" or "195-205°F" → normalise to Celsius
df['water_temp_c'] = df['water_temp'].apply(normalise_to_celsius)

df_clean = df.dropna(subset=['method_name', 'strength_score'])
df_clean.to_excel('Coffee_Brewing_Dashboard_Final.xlsx', index=False)
print(f"Clean dataset: {len(df_clean)} records")
```

---

##  Database — Supabase SQL

**Folder:** `sql/`

The cleaned dataset is stored in a Supabase PostgreSQL instance. The Streamlit app queries Supabase directly — meaning the recommendation engine always reads the latest data without redeploying.

```sql
-- Core table: brewing methods
CREATE TABLE brewing_methods (
    id                SERIAL PRIMARY KEY,
    method_name       TEXT NOT NULL,
    brew_time_min     NUMERIC,
    water_temp_c      NUMERIC,
    grind_size        TEXT,
    strength_score    INTEGER CHECK (strength_score BETWEEN 1 AND 10),
    acidity_score     INTEGER CHECK (acidity_score BETWEEN 1 AND 10),
    body_score        INTEGER CHECK (body_score BETWEEN 1 AND 10),
    difficulty        TEXT,
    recommended_roast TEXT[],
    bean_origins      TEXT[],
    flavour_notes     TEXT[],
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- Recommendation function: find best method by user preferences
CREATE OR REPLACE FUNCTION recommend_brewing_method(
    p_strength   INTEGER,
    p_acidity    INTEGER,
    p_body       INTEGER,
    p_difficulty TEXT DEFAULT NULL
)
RETURNS TABLE (
    method_name    TEXT,
    match_score    NUMERIC,
    brew_time_min  NUMERIC,
    water_temp_c   NUMERIC,
    grind_size     TEXT,
    flavour_notes  TEXT[]
)
LANGUAGE sql AS $$
    SELECT
        method_name,
        -- Euclidean distance inverted to a match score (0–100)
        ROUND(
            100 - SQRT(
                POWER(strength_score - p_strength, 2) +
                POWER(acidity_score  - p_acidity,  2) +
                POWER(body_score     - p_body,     2)
            ) * 5, 1
        ) AS match_score,
        brew_time_min,
        water_temp_c,
        grind_size,
        flavour_notes
    FROM brewing_methods
    WHERE (p_difficulty IS NULL OR difficulty = p_difficulty)
    ORDER BY match_score DESC
    LIMIT 5;
$$;
```

**Why Supabase instead of local PostgreSQL?**

Supabase is a hosted Postgres-as-a-service with a REST API and real-time subscriptions. The Streamlit app deployed on Streamlit Cloud can't maintain a connection to a local database — Supabase solves this with zero infrastructure management. Any update to the dataset in Supabase instantly reflects in the live app.

---

##  Dataset on Kaggle

>  **[Download dataset → kaggle.com/brianphu](https://www.kaggle.com/brianphu)**

| File | Rows | Description |
|------|------|-------------|
| `Coffee_Brewing_Methods_Raw.xlsx` | ~80 records | Raw scraped data pre-cleaning |
| `Coffee_Brewing_Dashboard_Final.xlsx` | ~80 records | Cleaned master dataset — used by Streamlit + Tableau |

**Column reference:**

| Column | Type | Example |
|--------|------|---------|
| `method_name` | string | V60 Pour Over |
| `brew_time_min` | float | 3.5 |
| `water_temp_c` | float | 93.0 |
| `grind_size` | string | Medium-Fine |
| `strength_score` | int (1–10) | 6 |
| `acidity_score` | int (1–10) | 8 |
| `body_score` | int (1–10) | 4 |
| `difficulty` | string | Intermediate |
| `recommended_roast` | list | Light, Medium |
| `bean_origins` | list | Ethiopia, Kenya |
| `flavour_notes` | list | Fruity, Floral, Bright |

---

##  Key Findings

### Finding 1 — Espresso is the outlier in every dimension

| Method | Strength | Acidity | Body | Brew Time |
|--------|---------|---------|------|-----------|
| Espresso | **9.5** | 6.0 | **9.0** | **0.5 min** |
| V60 | 5.5 | **8.5** | 3.5 | 3.5 min |
| French Press | 7.0 | 3.5 | **8.5** | 4.0 min |
| Cold Brew | 8.0 | 2.5 | 7.0 | 720 min |
| AeroPress | 7.5 | 5.5 | 6.0 | 2.0 min |
| Chemex | 5.0 | 7.5 | 2.5 | 5.0 min |

Espresso is the only method that simultaneously maximises strength *and* body in under one minute. Every other high-strength method trades off body or requires much longer brew times.

---

### Finding 2 — Acidity and body are inversely correlated across methods

| Correlation | Value | Interpretation |
|---|---|---|
| Acidity ↔ Body | **−0.71** | Strong inverse — bright coffees are thin; heavy coffees are flat |
| Strength ↔ Brew time | −0.43 | Medium inverse — faster methods are often stronger |
| Water temp ↔ Acidity | +0.38 | Slight positive — hotter water extracts more acids |

> This explains why French Press lovers rarely enjoy V60 and vice versa. It's not personal taste — it's physics. They occupy opposite ends of the acidity-body spectrum by design.

---

### Finding 3 — Ethiopian beans are the most versatile origin

| Origin | Compatible Methods | Peak Method | Avg Flavour Score |
|--------|-------------------|-------------|------------------|
| **Ethiopia** | **7** | V60, Chemex, Aeropress | 8.2 |
| Colombia | 6 | Drip, Pour Over, French Press | 7.6 |
| Brazil | 5 | Espresso, French Press, Moka Pot | 7.1 |
| Kenya | 4 | V60, Aeropress, Cold Brew | 8.0 |
| Guatemala | 4 | Drip, Chemex, French Press | 7.3 |

Ethiopian beans appeared in the top-performing combinations for 7 of 8 brewing methods — the only origin that works well across both high-acidity filter methods and lower-acidity immersion methods.

---

### Finding 4 — AeroPress is the beginner's shortcut to complex flavour

| Method | Difficulty | Flavour Complexity | Forgiving? |
|--------|-----------|-------------------|-----------|
| Espresso | Advanced | Very High | ❌ No |
| V60 | Intermediate | High | ❌ No |
| **AeroPress** | **Beginner** | **High** | **✅ Yes** |
| French Press | Beginner | Medium | ✅ Yes |
| Cold Brew | Beginner | Medium | ✅ Yes |
| Chemex | Intermediate | High | ❌ No |

AeroPress is the only method that combines beginner accessibility, forgiving technique tolerance, and genuinely complex flavour output. The data confirms what specialty coffee shops intuitively know — it's the gateway drug to serious brewing.

---

##  Full Data Pipeline

```
Coffee knowledge bases + specialty coffee blogs
│   (Perfect Daily Grind, Home Grounds, JavaPresse, etc.)
│
▼
Web Scraping (BeautifulSoup + Requests)
│   BREWING_METHODS_SCRAPING.ipynb
│
├── Extract: method name, brew parameters, flavour descriptors
├── Standardise: text → numeric scores (strength, acidity, body)
├── Normalise: temperatures to Celsius, times to minutes
└── Validate: remove duplicates, fill missing scores via cross-reference
│
▼
Coffee_Brewing_Methods_Raw.xlsx     ← raw scraped records
│
▼
Cleaning & Feature Engineering
│   BREWING_METHODS_SCRAPING.ipynb
│
├── Score normalisation (1–10 scale)
├── Flavour note tokenisation (list → comma-separated)
├── Difficulty classification (rule-based on parameter variance)
└── Bean origin compatibility scoring
│
▼
Coffee_Brewing_Dashboard_Final.xlsx ← clean master dataset
│
├──►  Kaggle: public dataset
│
├──► Supabase PostgreSQL
│    sql/ → recommend_brewing_method() stored function
│
├──► Tableau Public
│    Dashboard: method comparison / flavour matrix / origin map
│
├──► Google Colab Analysis
│    EDA + correlation analysis + clustering + Plotly charts
│
└──► Streamlit App (Coffee Beans Consultant)
     Coffee_Beans_Consultant_Streammlit_App/
     Supabase query → recommend_brewing_method() → ranked results
```

---

##  Technical Stack

| Layer | Tool | Why This Tool |
|---|---|---|
| Scraping | BeautifulSoup, Requests | Lightweight static HTML; no JavaScript rendering needed |
| Processing | Pandas, NumPy | Vectorised cleaning and score normalisation |
| Database | Supabase (PostgreSQL) | Hosted Postgres with REST API — no infra management, works with Streamlit Cloud |
| Recommendation logic | SQL stored function | Encapsulated server-side; any frontend calls one function |
| Visualisation (notebook) | Matplotlib, Seaborn, Plotly | Static EDA + interactive charts in same environment |
| Web app | Streamlit | Fastest path from Python + Supabase to deployed product |
| BI dashboard | Tableau Public | Stakeholder-facing, filter-driven comparison view |
| Deployment | Streamlit Cloud | Zero-infrastructure hosting; auto-deploys from GitHub |

### Why Supabase over local PostgreSQL?

Streamlit Cloud deployments can't connect to `localhost`. Supabase provides a hosted PostgreSQL instance with a stable connection string that works from anywhere — including Streamlit Cloud, Google Colab, and local development simultaneously. The `recommend_brewing_method()` function runs server-side, keeping recommendation logic decoupled from the app layer.

### Why score brewing parameters 1–10 instead of keeping raw values?

Raw values (brew time in minutes, temperature in °C, grind size as text) are incomparable. A Euclidean distance-based recommendation on raw values would weight temperature (range: 85–100°C) as 15× more important than brew time (range: 0.5–8 min) — which is meaningless. Normalising to 1–10 makes every dimension equally weighted in the similarity calculation.

---

##  Data Engineering

A runnable, tested ETL pipeline and SQLite star schema built from the files committed in this repo (no network calls; the scraping notebook is documented, not re-run).

```bash
pip install -r requirements-dev.txt
python -m pipeline            # extract -> validate -> transform -> load  (writes warehouse.db, docs/DATA_QUALITY.md)
python -m pipeline.docgen     # regenerate docs/DATA_DICTIONARY.md from the warehouse
python sql/run_queries.py     # run sql/analysis/*.sql -> docs/query_results/*.csv
python -m pytest -q           # 36 tests: pipeline, data quality, queries, docs freshness, app smoke test
```

| Stage | What it does | Code |
|---|---|---|
| Extract | Reads `coffee_dataset.csv`, the first sheet of `Coffee_Brewing_Dashboard_Final.xlsx`, and parses the beans, methods and `method_mapping` CTEs of the Streamlit SQL script | `pipeline/extract.py` |
| Validate | 44 checks (schema, nulls, duplicates, ranges, domains, referential, cross-source reconciliation); report in [`docs/DATA_QUALITY.md`](docs/DATA_QUALITY.md); errors block the load, known source quirks are reported as warnings | `pipeline/validate.py` |
| Transform | Cleans, maps bean brew-method labels to canonical methods, splits flavour notes into a bridge table, derives rating bands, ordinal encodings and caffeine/sleep labels | `pipeline/transform.py` |
| Load | Builds `warehouse.db` (gitignored) from `pipeline/schema.sql`: 6 dimensions, 1 fact, 1 bridge, FKs, CHECK constraints, indexes, a flat view | `pipeline/load.py` |

- **Model:** [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) (Mermaid ER diagram, grain, keys, provenance) and [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) (every column, generated from the warehouse).
- **Analysis SQL:** 10 SQLite queries in [`sql/analysis/`](sql/analysis/) (CTEs, `RANK`, `NTILE`, `PERCENT_RANK`, `LAG`, `FIRST_VALUE`, running totals, `CASE` pivots); outputs committed in [`docs/query_results/`](docs/query_results/).
- **Skills map:** [`docs/SKILLS_DEMONSTRATED.md`](docs/SKILLS_DEMONSTRATED.md).
- **Honest scope:** the committed files hold 32 beans and 13 brewing methods (the "~80" figure quoted elsewhere in this README is not reproduced by these files). The beans/ratings file has no documented source, and the method attributes are hard-coded dictionaries in the notebook (see the provenance table in the data model doc). With 32 rows, results are descriptive rather than statistically strong.

---

## Ingestion

Reusable ingestion module ported from the existing scraping notebook (`notebooks/BREWING_METHODS_SCRAPING.ipynb`). Only the sources and selectors the notebook already uses were ported.

```bash
pip install -r requirements-ingestion.txt
python -m ingestion.brewing_methods --out data/raw
python -m pytest -q tests/test_ingestion_*.py     # offline
```

Sources ported (the four in the notebook): Wikipedia (13 method pages), Healthline caffeine table, Perfect Daily Grind guide, National Coffee Association guide. Output: `data/raw/brewing_<source>.csv`. The notebook's hard-coded master dictionaries (brew time, caffeine, sensory scores) are curated values, not scraped, and are not part of ingestion. One deliberate deviation: the notebook's Perfect Daily Grind brew-time regex had a typo (`S]*`) that made it almost never match; it is corrected to the evident intent.

What it does: checks `robots.txt` (`urllib.robotparser`) and aborts politely if disallowed, sends an identifying User-Agent, waits at least 1 second between requests (default 1.5-2 s), retries with exponential backoff, caches raw HTML under `data/raw_html/` (git-ignored), and writes CSV with `scraped_at` and `source_url` columns. Parsing is separate from fetching: the parsers are pure functions of HTML text. Details in [docs/INGESTION.md](docs/INGESTION.md).

- **Parser verified on fixtures only.** The parser unit tests use small hand-written HTML fixtures (`tests/fixtures/`, labelled as not captured pages) that mimic the selectors the notebook uses.
- **Live run:** a manual GitHub Actions run fetched the sources from a hosted runner; results are in `docs/LIVE_RUN.md` (Wikipedia 13 rows, Healthline 3, NCA 5 headings with empty guide snippets). Perfect Daily Grind returned a bot challenge and is logged as 0 rows; no bypass is attempted. The notebook's selectors may drift as sites change.
- **Check the site's terms of use before running.** The fetcher reads `robots.txt` and stops if the URL is disallowed, but that is not a substitute for reading the terms.
- **For personal / portfolio use only.** Do not redistribute scraped content.

---

##  Project Structure

```
HEAD-BARISTA-COFFEE-INTELLIGENCE/
│
├── app.py                          # Streamlit app (reads coffee_dataset.csv)
├── coffee_dataset.csv              # Dataset used by the app
├── requirements.txt, requirements-dev.txt
│
├── notebooks/
│   └── BREWING_METHODS_SCRAPING.ipynb   # Scraping + cleaning pipeline
├── ingestion/                      # Reusable scraper modules (robots, rate limit, retries, cache) + fetch.py
├── data/
│   ├── Coffee_Brewing_Methods_Raw.xlsx      # Raw scraped data
│   └── Coffee_Brewing_Dashboard_Final.xlsx  # Cleaned dataset (Tableau / Excel dashboard)
├── sql/                            # SQL dataset scripts and CSV copy
│   ├── analysis/                   # 10 SQLite analytical queries
│   └── run_queries.py              # Runs them -> docs/query_results/*.csv
├── pipeline/                       # ETL: extract, validate, transform, load (SQLite star schema)
├── docs/                           # DATA_MODEL, DATA_DICTIONARY, DATA_QUALITY, SKILLS_DEMONSTRATED, query_results/
│
├── tests/                          # App smoke test, pipeline tests, query tests
└── .github/workflows/ci.yml        # Tests, end-to-end pipeline run, docs-freshness check
```

---

##  How to Run Locally

```bash
git clone https://github.com/brianphu2310/HEAD-BARISTA-COFFEE-INTELLIGENCE.git
cd HEAD-BARISTA-COFFEE-INTELLIGENCE

pip install -r requirements.txt
streamlit run app.py

# Optional: run the tests
pip install -r requirements-dev.txt && python -m pytest -q
```

**Or run the scraping notebook:**

```bash
jupyter notebook notebooks/BREWING_METHODS_SCRAPING.ipynb
```

**Want the data without scraping?** Download directly from Kaggle:

```bash
kaggle datasets download brianphu/head-barista-coffee-intelligence
```

---

##  Limitations & What I'd Do With More Data

The dataset covers ~80 brewing methods and configurations. That's enough to build a working recommender, but not enough to capture the full complexity of speciality coffee.

With more data I would:

- **Add user feedback loop** — the Streamlit app currently recommends but doesn't learn. Adding a "was this helpful?" button and storing responses in Supabase would let the recommendation function improve over time through a simple feedback weighting system
- **Include bean varietal data** — the current dataset treats origin as a proxy for flavour (Ethiopia ≈ fruity). In reality, a Yirgacheffe and a Sidama are both Ethiopian but taste completely different. Varietal-level data would make recommendations dramatically more precise
- **Model seasonal extraction variance** — humidity and ambient temperature affect extraction; a barista's ideal parameters in Sydney summer differ from Sydney winter. Adding a `season` parameter to the recommendation function would make it genuinely location-aware
- **Scrape customer reviews** — Yelp and Google Maps reviews for cafés often mention brewing methods and flavour notes. NLP sentiment analysis on those reviews would validate whether the structured flavour scores in this dataset actually match how real customers experience the coffee

---

##  About

**Brian Phu** — Data Analyst & Former Barista, Sydney

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/brian-phu-data-analysta55353390/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/brianphu2310)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=flat&logo=kaggle&logoColor=white)](https://www.kaggle.com/brianphu)
[![Tableau](https://img.shields.io/badge/Tableau-E97627?style=flat&logo=tableau&logoColor=white)](https://public.tableau.com/app/profile/brian.ma5935/vizzes)

> *"I used to answer 'which coffee is better?' from behind a counter, with nothing but experience and instinct. This project is my attempt to answer the same question with data. The answer is still complicated — but now I can show my working."*

---

**Last updated:** May 2026 &nbsp;|&nbsp; **Brewing methods analysed:** ~80 &nbsp;|&nbsp; **Sources scraped:** 3+ &nbsp;|&nbsp; **Dashboards:** 3 (Streamlit, Colab, Tableau) &nbsp;|&nbsp; One former barista who asks too many questions

---

*MIT License — free to use, modify, and share.*
