# 🏦 Dividend Analysis & Visualization of Polish Companies

## 📘 Project Description

This project analyzes the **dividend performance, consistency, and sector trends** of companies listed on the Polish stock market.

It demonstrates the creation of a **complete analytics pipeline**, from data collection and transformation to interactive visualization, using:

- **Python** → Data scraping and preprocessing  
- **PostgreSQL** → Data storage and analytical SQL views  
- **Power BI (DirectQuery)** → Dynamic dashboards for live analytics  
- *(Future)* **Machine Learning** → Dividend yield prediction models  

---

## 🎯 Project Objectives

- Analyze dividend trends by company and sector  
- Identify the most consistent dividend-paying companies  
- Visualize historical yield and sector performance interactively  
- Build a foundation for future **dividend prediction models**

---


### 1️⃣ Data Collection
Python scripts scrape dividend and stock data for Polish companies.

### 2️⃣ Data Storage
Data stored in PostgreSQL schema:
- `stock_data.companies`
- `stock_data.stock_data`
- `stock_data.dividend_data`

### 3️⃣ Data Transformation
Custom SQL views are built for analysis:
- Company Dividend Yield  
- Sector Year-over-Year Growth  
- Top Dividend Payers  
- Dividend Consistency (streaks)

### 4️⃣ Visualization
Interactive dashboards created in Power BI using **DirectQuery** for real-time updates.

---

## 🧩 SQL Views Overview

| View | Purpose |
|------|----------|
| `company_dividend_yield` | Annual dividend yield per company |
| `sector_yoy_growth` | Year-over-year growth in sector volumes |
| `top_dividend_payers` | Ranking of top dividend-paying companies |
| `dividend_consistency` | Dividend streaks and consistency per company |

---

## 📊 Power BI Dashboards

### 🔹 Dashboard 1 — Dividend Overview

<img width="1310" height="718" alt="obraz" src="https://github.com/user-attachments/assets/4234b4d9-e0e4-4a16-b4a7-1a946db04a29" />

**Contains:**  
- Market average dividend yield KPI  
- Top dividend-paying companies  
- Year-over-year yield trend line  
- Sector performance heatmap  

---

### 🔹 Dashboard 2 — Dividend Consistency & Reliability
  
<img width="1305" height="721" alt="obraz" src="https://github.com/user-attachments/assets/3fe04085-8367-4cbf-9c6b-d4ecfbe4af65" />


**Contains:**  
- Longest dividend streaks  
- Dividend-paying consistency across sectors  
- Stacked column chart of yearly growth by sector  
- Sector reliability ranking  

---

### 🔹 (Planned) Dashboard 3 — Dividend Forecasts

---

## ⚙️ Tech Stack

| Layer | Tool |
|-------|------|
| Data Storage | PostgreSQL |
| Data Processing | SQL (CTEs & Views) |
| Visualization | Power BI (DirectQuery) |
| Scripting (Future) | Python |
| Deployment | Local / AWS (Planned) |

---

## 📁 Repository Structure

<img width="187" height="714" alt="obraz" src="https://github.com/user-attachments/assets/a0770567-f821-4a9e-962e-96658d49cfb7" />


## 🚀 How to Run

1. Import SQL views into PostgreSQL.  
2. Connect Power BI to PostgreSQL using DirectQuery.  
3. Open the `.pbip` Power BI project file.  
4. Interact with visuals — data updates automatically when PostgreSQL data changes.  

---

## 🔮 Future Development

- [ ] Add ML model for dividend yield prediction  
- [ ] Automate data refresh pipeline  
- [ ] Deploy dashboard to Power BI Service / AWS  
- [ ] Build REST API endpoint for dynamic querying  

