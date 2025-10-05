WITH basic_info AS (
    SELECT
        ticker,
        company_name,
        sector
    FROM stock_data.companies
),
number_of_dividends AS (
    SELECT
        ticker,
        COUNT(dividend) AS dividend_count
    FROM stock_data.dividend_data
    GROUP BY 1
    HAVING COUNT(date) > 0
),
annual_dividends AS (
    SELECT
        ticker,
        EXTRACT(YEAR FROM date) AS year,
        SUM(dividend) AS total_annual_dividend
    FROM stock_data.dividend_data
    GROUP BY 1, 2
),
dividend_flags AS (
    SELECT
        ticker,
        year,
        CASE WHEN total_annual_dividend > 0 THEN 1 ELSE 0 END AS dividend_paid
    FROM annual_dividends
),
streak_groups AS (
    SELECT
        ticker,
        year,
        dividend_paid,
        year - ROW_NUMBER() OVER(PARTITION BY ticker ORDER BY year) AS grp
    FROM dividend_flags
    WHERE dividend_paid = 1
),
streak_lengths AS (
    SELECT
        ticker,
        grp,
        COUNT(*) AS streak_length
    FROM streak_groups
    GROUP BY ticker, grp
),
longest_streak AS (
    SELECT
        ticker,
        MAX(streak_length) AS longest_streak
    FROM streak_lengths
    GROUP BY ticker
)

SELECT
    bi.ticker,
    bi.company_name,
    bi.sector,
    COALESCE(nod.dividend_count, 0) AS dividend_count,
    COALESCE(ls.longest_streak, 0) AS longest_streak
FROM basic_info bi
LEFT JOIN number_of_dividends nod
    ON bi.ticker = nod.ticker
LEFT JOIN longest_streak ls
    ON bi.ticker = ls.ticker
ORDER BY ls.longest_streak DESC NULLS LAST, nod.dividend_count DESC;
