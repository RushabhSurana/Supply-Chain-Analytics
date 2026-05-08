# 🚢 Supply Chain Analytics

> **Identifying Delay Drivers & Optimising Logistics Performance Across India-Centric Global Trade Routes**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/supply-chain-analytics/blob/main/notebooks/Supply_Chain_Analytics.ipynb)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen)]()

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Key Findings](#-key-findings)
- [Repository Structure](#-repository-structure)
- [Getting Started](#-getting-started)
- [Project Phases](#-project-phases)
- [Dataset](#-dataset)
- [Tech Stack](#-tech-stack)
- [Team](#-team)

---

## 📌 Project Overview

This project delivers an **end-to-end supply chain analytics pipeline** on 728 India-centric import/export shipments spanning January 2024 to December 2025 ($101.8M total trade value).

The core business question: **which shipments are most likely to be delayed, and what can logistics teams do about it before dispatch?**

We answer this through:
- Systematic data auditing and root-cause cleaning
- Exploratory analysis across product categories, trade routes, and customs timelines
- Conditional delay probability tables and a predictive ML model
- Interactive visualisations (Sankey diagrams, choropleth maps, heatmaps)
- SQL-powered reporting queries
- GenAI-generated operational recommendations via the Anthropic Claude API

---

## 📊 Key Findings

| Metric | Value |
|--------|-------|
| Overall delay rate | **15.9%** (116 of 728 shipments) |
| Highest-risk route | **Mumbai → Singapore (25.0% delay rate)** |
| Highest-risk category | **Consumer Goods (17.5%)** |
| Highest-risk origin | **Germany (23.1%)** |
| Customs clearance impact | Delayed shipments average **4.9 days** vs 3.6 days for on-time |
| Data quality issue found | **24 rows** with systematic 3-column corruption — fully recovered |

### 🔴 Top Recommendations

1. **Mumbai → Singapore**: Initiate pre-clearance documentation 72 hrs before dispatch; evaluate alternate carriers
2. **Consumer Goods**: Assign dedicated customs compliance agent; standardise documentation checklist
3. **Customs >4 days**: Implement automated document review flag for at-risk shipments
4. **Germany origin**: Build 2-day SLA buffer; review vendor lead time compliance

---

## 📁 Repository Structure

```
supply-chain-analytics/
│
├── 📄 README.md                          ← You are here
├── 📄 requirements.txt                   ← Python dependencies
├── 📄 LICENSE
│
├── 📂 data/
│   ├── 📂 raw/
│   │   └── shipment.csv                  ← Original dataset (never modified)
│   └── 📂 processed/
│       └── shipment_cleaned.csv          ← Output of Phase 2 cleaning
│
├── 📂 notebooks/
│   └── Supply_Chain_Analytics.ipynb      ← Main project notebook (all 8 phases)
│
├── 📂 scripts/
│   └── data_cleaning.py                  ← Standalone cleaning script (Phase 2)
│
├── 📂 sql/
│   └── queries.sql                       ← 6 business SQL queries (Phase 7)
│
└── 📂 presentation/
    └── Supply_Chain_Analytics.pptx       ← Final project presentation (15 slides)
```

---

## 🚀 Getting Started

### Option 1 — Google Colab (Recommended, zero setup)

Click the badge at the top of this README, or use this link:

```
https://colab.research.google.com/github/YOUR_USERNAME/supply-chain-analytics/blob/main/notebooks/Supply_Chain_Analytics.ipynb
```

When the notebook opens:
1. Run the **Setup cell** first (installs plotly, imports all libraries)
2. In **Phase 2**, upload `data/raw/shipment.csv` when prompted
3. Run cells top to bottom — each phase builds on the previous

### Option 2 — Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/supply-chain-analytics.git
cd supply-chain-analytics

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Jupyter
jupyter notebook notebooks/Supply_Chain_Analytics.ipynb
```

### Option 3 — Run the cleaning script only

```bash
# Place shipment.csv in the same directory, then:
python scripts/data_cleaning.py
# Output: shipment_cleaned.csv
```

---

## 🔄 Project Phases

| Phase | Title | Owner | Description |
|-------|-------|-------|-------------|
| 1 | Business Questions | Member 1 | Define 4 core analytical questions |
| 2 | Data Audit & Cleaning | Member 2 | Identify and fix all data quality issues |
| 3 | Feature Engineering | Member 3 | Create 9 derived analytical columns |
| 4 | EDA | Member 4 | Univariate, bivariate, and time-based analysis |
| 5 | Delay Probability Analysis | Member 5 | Conditional probabilities + ML model |
| 6 | Visualisation | Member 6 | Sankey, heatmap, choropleth, bar charts |
| 7 | SQL Queries | Members 1 & 2 | 6 business reporting queries on SQLite |
| 8 | GenAI Optimisation | Members 3 & 4 | Claude API-powered recommendations |

---

## 📦 Dataset

| Property | Value |
|----------|-------|
| File | `data/raw/shipment.csv` |
| Rows | 728 shipments |
| Columns | 12 raw + 9 engineered |
| Date range | January 2024 – December 2025 |
| Trade volume | $101.8M |
| Categories | Electronics, Textiles, Consumer Goods, Industrial Equipment |
| Countries | 15 origin/destination countries |
| Target variable | `delivery_status` (On-Time / Delayed) |

### Data Quality Issues Found & Fixed

> **Root cause:** 24 Industrial Equipment Export→Singapore rows had a systematic 3-column misalignment during data entry. All values were fully recovered — zero rows dropped.

| Column | Issue | Fix Applied |
|--------|-------|-------------|
| `delivery_status` | 24 NaN values | Rescued from `customs_clearance_time_days` column |
| `customs_clearance_time_days` | Text values in 24 rows | Converted to float64; bad entries → NaN + flagged |
| `D_Country` | Numeric strings in 24 rows | Set to 'Singapore' (confirmed via `destination` column) |
| `date` | Stored as plain string | Converted to datetime64 |
| All text columns | Inconsistent whitespace/casing | Stripped and title-cased |

---

## 🛠 Tech Stack

| Layer | Tools |
|-------|-------|
| **Language** | Python 3.10+ |
| **Data** | Pandas, NumPy |
| **Visualisation** | Matplotlib, Seaborn, Plotly |
| **Machine Learning** | Scikit-learn (Logistic Regression, Decision Tree) |
| **SQL** | SQLite (in-memory via Python `sqlite3`) |
| **AI** | Anthropic Claude API (`claude-sonnet-4-20250514`) |
| **Environment** | Google Colab / Jupyter Notebook |
| **Version Control** | Git + GitHub |

---

## 👥 Team

| Member | Phase Ownership |
|--------|----------------|
| Member 1 | Business Questions (Phase 1) · SQL Queries (Phase 7) |
| Member 2 | Data Audit & Cleaning (Phase 2) · SQL Schema (Phase 7) |
| Member 3 | Feature Engineering (Phase 3) · GenAI Prompting (Phase 8) |
| Member 4 | EDA (Phase 4) · GenAI Summaries (Phase 8) |
| Member 5 | Delay Probability Analysis & ML Model (Phase 5) |
| Member 6 | Visualisations & Charts (Phase 6) · Presentation (Phase 6) |

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

*Supply Chain Analytics Project · Consulting Analytics Group*
