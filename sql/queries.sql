-- ============================================================
-- Supply Chain Analytics — Business SQL Queries
-- Phase 7 | Members 1 & 2
-- Database: SQLite (compatible with PostgreSQL with minor changes)
-- Table: shipments (load from shipment_cleaned.csv)
-- ============================================================

-- HOW TO USE:
-- In the notebook, the table is loaded automatically via:
--   df.to_sql('shipments', conn, if_exists='replace', index=False)
-- You can also run these queries in DB Browser for SQLite
-- by importing shipment_cleaned.csv as a table named 'shipments'.


-- ─────────────────────────────────────────────────────────────
-- Q1: Which trade routes have the highest delay rates?
--     Answers: Business Question 1 (Where are delays happening?)
-- ─────────────────────────────────────────────────────────────
SELECT
    origin || ' → ' || destination          AS route,
    COUNT(*)                                 AS total_shipments,
    SUM(is_delayed)                          AS delayed_count,
    ROUND(AVG(is_delayed) * 100, 1)          AS delay_rate_pct,
    ROUND(AVG(freight_cost), 0)              AS avg_freight_usd
FROM shipments
GROUP BY route
HAVING total_shipments >= 3
ORDER BY delay_rate_pct DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- Q2: Average freight cost and efficiency by product category
--     Answers: Business Question 4 (expensive routes = delayed routes?)
-- ─────────────────────────────────────────────────────────────
SELECT
    product_category,
    COUNT(*)                                 AS shipments,
    ROUND(AVG(freight_cost), 0)              AS avg_freight_usd,
    ROUND(AVG(value), 0)                     AS avg_value_usd,
    ROUND(AVG(CAST(freight_cost AS FLOAT) / value), 4)  AS avg_freight_ratio,
    ROUND(AVG(is_delayed) * 100, 1)          AS delay_rate_pct
FROM shipments
GROUP BY product_category
ORDER BY avg_freight_usd DESC;


-- ─────────────────────────────────────────────────────────────
-- Q3: Delay rate and avg customs clearance by origin country
--     Answers: Business Question 2 (which origins drive delays?)
-- ─────────────────────────────────────────────────────────────
SELECT
    O_Country,
    COUNT(*)                                 AS total_shipments,
    SUM(is_delayed)                          AS delayed_count,
    ROUND(AVG(is_delayed) * 100, 1)          AS delay_rate_pct,
    ROUND(AVG(customs_clearance_time_days), 2) AS avg_clearance_days
FROM shipments
WHERE customs_clearance_time_days IS NOT NULL
GROUP BY O_Country
ORDER BY delay_rate_pct DESC;


-- ─────────────────────────────────────────────────────────────
-- Q4: Destination country breakdown — volume, type, delay, value
-- ─────────────────────────────────────────────────────────────
SELECT
    D_Country,
    COUNT(*)                                       AS total_shipments,
    SUM(CASE WHEN type = 'Import' THEN 1 ELSE 0 END) AS imports,
    SUM(CASE WHEN type = 'Export' THEN 1 ELSE 0 END) AS exports,
    ROUND(AVG(is_delayed) * 100, 1)                AS delay_rate_pct,
    ROUND(SUM(value) / 1000000.0, 2)               AS total_value_million_usd
FROM shipments
GROUP BY D_Country
ORDER BY total_shipments DESC;


-- ─────────────────────────────────────────────────────────────
-- Q5: Monthly delay trend — Jan 2024 to Dec 2025
--     Answers: Business Question 1 (time-based delay patterns)
-- ─────────────────────────────────────────────────────────────
SELECT
    SUBSTR(date, 1, 7)                       AS year_month,
    COUNT(*)                                  AS total_shipments,
    SUM(is_delayed)                           AS delayed_count,
    ROUND(AVG(is_delayed) * 100, 1)           AS delay_rate_pct
FROM shipments
GROUP BY year_month
ORDER BY year_month;


-- ─────────────────────────────────────────────────────────────
-- Q6: High-value shipment delay risk by category and lane
--     Answers: which high-value lanes need the most protection?
-- ─────────────────────────────────────────────────────────────
SELECT
    product_category,
    O_Country,
    D_Country,
    COUNT(*)                                  AS high_value_shipments,
    SUM(is_delayed)                           AS delayed_count,
    ROUND(AVG(is_delayed) * 100, 1)           AS delay_rate_pct,
    ROUND(AVG(value), 0)                      AS avg_value_usd
FROM shipments
WHERE high_value_shipment = 1
GROUP BY product_category, O_Country, D_Country
HAVING high_value_shipments >= 3
ORDER BY delay_rate_pct DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- BONUS — Customs clearance bucket delay summary
--         Answers: Business Question 3 (customs → delays?)
-- ─────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN customs_clearance_time_days <= 2.5 THEN 'Low (≤2.5 days)'
        WHEN customs_clearance_time_days <= 4.0 THEN 'Medium (2.5–4 days)'
        ELSE 'High (>4 days)'
    END                                       AS clearance_tier,
    COUNT(*)                                  AS shipments,
    SUM(is_delayed)                           AS delayed,
    ROUND(AVG(is_delayed) * 100, 1)           AS delay_rate_pct
FROM shipments
WHERE customs_clearance_time_days IS NOT NULL
GROUP BY clearance_tier
ORDER BY delay_rate_pct DESC;
