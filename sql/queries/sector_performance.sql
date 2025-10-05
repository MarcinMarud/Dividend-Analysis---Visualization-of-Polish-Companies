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
yoy_div_growth AS (
	SELECT
		ad.year,
		ad.ticker,
		(ad.total_annual_dividend / aac.avg_annual_close_price) * 100 AS dividend_yield
	FROM annual_dps ad
	JOIN annual_avg_close aac
		ON ad.year = aac.year
		AND ad.ticker = aac.ticker	
),
yoy_div_pct AS (
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
	FROM yoy_div_growth yoy
	JOIN stock_data.companies c
		ON yoy.ticker = c.ticker
),
volume AS (
	SELECT
		c.sector,
		EXTRACT(YEAR FROM sd.date) AS year,
		SUM(sd.volume) AS total_volume
	FROM stock_data.stock_data sd
	JOIN stock_data.companies c
		ON sd.ticker = c.ticker
	GROUP BY 1, 2
),
avg_sector_yield AS (
	SELECT
		yoydp.sector,
		yoydp.year,
		ROUND(AVG(yoydp.yoy_dividend_yield), 2) AS average_sector_dividend_yield
	FROM yoy_div_pct yoydp
	JOIN volume v
		ON yoydp.sector = v.sector
		AND yoydp.year = v.year
	GROUP BY 1,2
),
sector_yield_growth AS (
	SELECT
		asy.sector,
		asy.year,
		LAG(asy.average_sector_dividend_yield) OVER(PARTITION BY asy.sector ORDER BY asy.year) as prev_sector_dividend_yield
	FROM avg_sector_yield asy
),
sector_volume_growth AS (
	SELECT
		v.sector,
		v.year,
		LAG(v.total_volume) OVER(PARTITION BY v.sector ORDER BY v.year) AS prev_volume
	FROM volume v
)

SELECT 
	asdy.sector,
	asdy.year,
	asdy.average_sector_dividend_yield,
	v.total_volume,
	COALESCE(
		ROUND(
			((asdy.average_sector_dividend_yield - syg.prev_sector_dividend_yield) / syg.prev_sector_dividend_yield) 
			* 100,
		2)
	, 0) AS yoy_sector_dividend_yield_growth,
	COALESCE(
		ROUND(
			((v.total_volume - svg.prev_volume) / svg.prev_volume) 
			* 100,
		2)
	, 0) AS yoy_sector_dividend_volume_growth
FROM avg_sector_yield asdy
JOIN volume v
	ON asdy.sector = v.sector
	AND asdy.year = v.year
JOIN sector_yield_growth syg
	ON asdy.sector = syg.sector
	AND asdy.year = syg.year
JOIN sector_volume_growth svg
	ON asdy.sector = svg.sector
	AND asdy.year = svg.year
	





