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
),
overall_avg_yield AS (
	SELECT
		yoy.ticker,
		AVG(yoy.dividend_yield) AS avg_overall_dividend_yield
	FROM yoy_growth yoy
	GROUP BY 1
)

SELECT 
	oay.ticker,
	c.company_name,
	c.sector,
	ROUND(oay.avg_overall_dividend_yield, 2) AS avg_overall_dividend_yield,
	RANK() OVER(ORDER BY oay.avg_overall_dividend_yield DESC) AS rnk
FROM overall_avg_yield oay
JOIN stock_data.companies c
	ON oay.ticker = c.ticker