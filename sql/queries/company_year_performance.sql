WITH annual_dps AS (
  SELECT
    EXTRACT(YEAR FROM date) AS year,
    Ticker,
    SUM(Dividend) AS total_annual_dividend
  FROM stock_data.dividend_data
  GROUP BY 1, 2
),
annual_avg_close AS (
  SELECT
    EXTRACT(YEAR FROM date) AS year,
    Ticker,
    AVG(Close) AS avg_annual_close_price
  FROM stock_data.stock_data
  GROUP BY 1, 2
),
yoy_growth AS (
	SELECT
		ad.year,
		ad.ticker,
		(ad.total_annual_dividend / aac.avg_annual_close_price) * 100 AS dividend_yield
	FROM annual_dps ad
	JOIN annual_avg_close aac
		ON ad.year = aac.year
		AND ad.ticker = aac.ticker	
)

SELECT 
	yoy.year,
	yoy.ticker,
	c.company_name,
	c.sector,
	ROUND(yoy.dividend_yield, 2) AS yoy_dividend_yield,
	COALESCE(
		ROUND(
			((yoy.dividend_yield - LAG(yoy.dividend_yield) OVER(PARTITION BY yoy.ticker ORDER BY yoy.year)) /
			LAG(yoy.dividend_yield) OVER(PARTITION BY yoy.ticker ORDER BY yoy.year))
		, 2)
	, 0) * 100 AS yoy_dividend_growth
FROM yoy_growth yoy
JOIN stock_data.companies c
	ON yoy.ticker = c.ticker