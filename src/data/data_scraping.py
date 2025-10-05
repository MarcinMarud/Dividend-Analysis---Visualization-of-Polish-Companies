#!/usr/bin/env python3

import yfinance as yf
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import time
import warnings
warnings.filterwarnings('ignore')


class PolishDividendScraper:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        self.raw_data_path = os.path.join(project_root, "scraped_data", "raw")
        print(f"Raw data path: {self.raw_data_path}")
        self.create_directories()

        self.polish_companies = {
            "PKO.WA": {"name": "PKO Bank Polski", "sector": "Banking", "industry": "Banks"},
            "PEO.WA": {"name": "Bank Pekao", "sector": "Banking", "industry": "Banks"},
            "SPL.WA": {"name": "Santander Bank Polska", "sector": "Banking", "industry": "Banks"},
            "MBK.WA": {"name": "mBank", "sector": "Banking", "industry": "Banks"},
            "ING.WA": {"name": "ING Bank Śląski", "sector": "Banking", "industry": "Banks"},
            "MIL.WA": {"name": "Bank Millennium", "sector": "Banking", "industry": "Banks"},
            "ALR.WA": {"name": "Alior Bank", "sector": "Banking", "industry": "Banks"},
            "BHW.WA": {"name": "Bank Handlowy", "sector": "Banking", "industry": "Banks"},
            "BNP.WA": {"name": "BNP Paribas Bank Polska", "sector": "Banking", "industry": "Banks"},
            "PKN.WA": {"name": "PKN Orlen", "sector": "Energy", "industry": "Oil & Gas"},
            "PGE.WA": {"name": "PGE Polska Grupa Energetyczna", "sector": "Utilities", "industry": "Electric Utilities"},
            "TPE.WA": {"name": "TAURON Polska Energia", "sector": "Utilities", "industry": "Electric Utilities"},
            "ENG.WA": {"name": "Energa", "sector": "Utilities", "industry": "Electric Utilities"},
            "ENA.WA": {"name": "ENEA", "sector": "Utilities", "industry": "Electric Utilities"},
            "PZU.WA": {"name": "PZU", "sector": "Insurance", "industry": "Insurance"},
            "KGH.WA": {"name": "KGHM Polska Miedź", "sector": "Materials", "industry": "Industrial Metals & Mining"},
            "JSW.WA": {"name": "Jastrzębska Spółka Węglowa", "sector": "Energy", "industry": "Coal"},
            "ATT.WA": {"name": "Grupa Azoty", "sector": "Materials", "industry": "Chemicals"},
            "LWB.WA": {"name": "Lubelski Węgiel Bogdanka", "sector": "Energy", "industry": "Coal"},
            "CDR.WA": {"name": "CD Projekt", "sector": "Technology", "industry": "Software & Games"},
            "ACP.WA": {"name": "Asseco Poland", "sector": "Technology", "industry": "Software"},
            "OPL.WA": {"name": "Orange Polska", "sector": "Telecommunications", "industry": "Telecom Services"},
            "CPS.WA": {"name": "Cyfrowy Polsat", "sector": "Telecommunications", "industry": "Media & Broadcasting"},
            "ASE.WA": {"name": "Asseco South Eastern Europe", "sector": "Technology", "industry": "Software"},
            "DNP.WA": {"name": "Dino Polska", "sector": "Consumer Staples", "industry": "Food Retail"},
            "ALE.WA": {"name": "Allegro.eu", "sector": "Consumer Discretionary", "industry": "E-commerce"},
            "LPP.WA": {"name": "LPP", "sector": "Consumer Discretionary", "industry": "Apparel Retail"},
            "CCC.WA": {"name": "CCC", "sector": "Consumer Discretionary", "industry": "Footwear Retail"},
            "ZAB.WA": {"name": "Żabka Group", "sector": "Consumer Staples", "industry": "Convenience Stores"},
            "BDX.WA": {"name": "Budimex", "sector": "Industrials", "industry": "Construction"},
            "DOM.WA": {"name": "Dom Development", "sector": "Real Estate", "industry": "Real Estate Development"},
            "ECH.WA": {"name": "Echo Investment", "sector": "Real Estate", "industry": "Real Estate Development"},
            "1AT.WA": {"name": "Atal", "sector": "Real Estate", "industry": "Real Estate Development"},
            "KTY.WA": {"name": "Grupa Kęty", "sector": "Materials", "industry": "Aluminum"},
            "CAR.WA": {"name": "Inter Cars", "sector": "Consumer Discretionary", "industry": "Auto Parts"},
            "KRU.WA": {"name": "KRUK", "sector": "Financial Services", "industry": "Debt Collection"},
            "WLT.WA": {"name": "Wielton", "sector": "Industrials", "industry": "Commercial Vehicles"},
            "BFT.WA": {"name": "Benefit Systems", "sector": "Consumer Discretionary", "industry": "Leisure Services"},
            "XTB.WA": {"name": "XTB", "sector": "Financial Services", "industry": "Online Brokerage"},
            "DIA.WA": {"name": "Diagnostyka", "sector": "Healthcare", "industry": "Medical Diagnostics"},
            "KER.WA": {"name": "Kernel Holding", "sector": "Consumer Staples", "industry": "Food Processing"},
            "PEP.WA": {"name": "Polenergia", "sector": "Utilities", "industry": "Renewable Energy"},
            "EAT.WA": {"name": "AmRest Holdings", "sector": "Consumer Discretionary", "industry": "Restaurants"},
            "NEU.WA": {"name": "NEUCA", "sector": "Consumer Staples", "industry": "Food Distribution"},
        }
        print(f"Total companies to scrape: {len(self.polish_companies)}")

    def create_directories(self):
        directories = [
            self.raw_data_path,
            os.path.join(self.raw_data_path, "stock_data"),
            os.path.join(self.raw_data_path, "dividend_data"),
            os.path.join(self.raw_data_path, "financial_data"),
            os.path.join(self.raw_data_path, "company_info"),
            os.path.join(self.raw_data_path, "metadata")
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"Directory created: {directory}")

    def get_stock_data(self, ticker: str, period: str = "10y"):
        try:
            print(f"Getting stock data for {ticker}")
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            if hist.empty:
                print(f"No stock data for {ticker}")
                return None
            hist['Ticker'] = ticker
            hist['Date'] = hist.index
            hist.reset_index(drop=True, inplace=True)
            print(f"Got {len(hist)} stock records for {ticker}")
            return hist
        except Exception as e:
            print(f"Error getting stock data for {ticker}: {e}")
            return None

    def get_dividend_data(self, ticker: str):
        try:
            print(f"Getting dividend data for {ticker}")
            stock = yf.Ticker(ticker)
            dividends = stock.dividends
            if dividends.empty:
                print(f"No dividend data for {ticker}")
                return None
            div_df = dividends.reset_index()
            div_df.columns = ['Date', 'Dividend']
            div_df['Ticker'] = ticker
            print(f"Got {len(div_df)} dividend records for {ticker}")
            return div_df
        except Exception as e:
            print(f"Error getting dividend data for {ticker}: {e}")
            return None

    def get_financial_data(self, ticker: str):
        try:
            print(f"Getting financial data for {ticker}")
            stock = yf.Ticker(ticker)
            info = stock.info
            financials = stock.financials
            balance_sheet = stock.balance_sheet
            cashflow = stock.cashflow

            financial_data = {
                'ticker': ticker,
                'info': info,
                'financials': financials.to_dict() if not financials.empty else {},
                'balance_sheet': balance_sheet.to_dict() if not balance_sheet.empty else {},
                'cashflow': cashflow.to_dict() if not cashflow.empty else {},
                'scraped_date': datetime.now().isoformat()
            }
            print(f"Got financial data for {ticker}")
            return financial_data
        except Exception as e:
            print(f"Error getting financial data for {ticker}: {e}")
            return {}

    def save_data(self, data, filename: str, subfolder: str):
        try:
            filepath = os.path.join(self.raw_data_path, subfolder, filename)
            data.to_csv(filepath, index=False)
            print(f"Saved data to {filepath}")
        except Exception as e:
            print(f"Error saving {filename}: {e}")

    def convert_timestamps(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                # Convert timestamp keys to strings
                if isinstance(key, pd.Timestamp):
                    new_key = key.isoformat()
                else:
                    new_key = str(key)
                new_dict[new_key] = self.convert_timestamps(value)
            return new_dict
        elif isinstance(obj, list):
            return [self.convert_timestamps(item) for item in obj]
        elif isinstance(obj, (np.int64, np.float64)):
            return float(obj)
        elif pd.isna(obj):
            return None
        else:
            return obj

    def save_json(self, data, filename: str, subfolder: str):
        try:
            filepath = os.path.join(self.raw_data_path, subfolder, filename)
            clean_data = self.convert_timestamps(data)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(clean_data, f, indent=2,
                          default=str, ensure_ascii=False)
            print(f"Saved JSON to {filepath}")
        except Exception as e:
            print(f"Error saving JSON {filename}: {e}")

    def scrape_all_companies(self):
        print("Starting scraping process...")
        all_stock_data = []
        all_dividend_data = []
        company_metadata = []
        successful = 0
        failed = 0

        for i, (ticker, company_info) in enumerate(self.polish_companies.items(), 1):
            print(
                f"\nProcessing {i}/{len(self.polish_companies)}: {ticker} - {company_info['name']}")

            try:
                metadata = {
                    'ticker': ticker,
                    'company_name': company_info['name'],
                    'sector': company_info['sector'],
                    'industry': company_info['industry'],
                    'scrape_date': datetime.now().isoformat()
                }
                company_metadata.append(metadata)

                stock_data = self.get_stock_data(ticker)
                if stock_data is not None:
                    stock_data['sector'] = company_info['sector']
                    stock_data['industry'] = company_info['industry']
                    stock_data['company_name'] = company_info['name']
                    all_stock_data.append(stock_data)

                div_data = self.get_dividend_data(ticker)
                if div_data is not None:
                    div_data['sector'] = company_info['sector']
                    div_data['industry'] = company_info['industry']
                    div_data['company_name'] = company_info['name']
                    all_dividend_data.append(div_data)

                financial_data = self.get_financial_data(ticker)
                if financial_data:
                    financial_data.update(company_info)
                    self.save_json(
                        financial_data, f"{ticker}_financial_data.json", "financial_data")

                successful += 1
                print(f"Successfully processed {ticker}")
                time.sleep(1)

            except Exception as e:
                print(f"Failed to process {ticker}: {e}")
                failed += 1
                continue

        print(f"\nSaving combined data files...")

        if all_stock_data:
            combined_stock_data = pd.concat(all_stock_data, ignore_index=True)
            self.save_data(combined_stock_data,
                           "all_stock_data.csv", "stock_data")
            print(
                f"Combined stock data: {len(combined_stock_data)} total records")

        if all_dividend_data:
            combined_div_data = pd.concat(all_dividend_data, ignore_index=True)
            self.save_data(combined_div_data,
                           "all_dividend_data.csv", "dividend_data")
            print(
                f"Combined dividend data: {len(combined_div_data)} total records")

        if company_metadata:
            metadata_df = pd.DataFrame(company_metadata)
            self.save_data(metadata_df, "company_metadata.csv", "metadata")
            print(f"Company metadata: {len(metadata_df)} companies")

        print(f"\nScraping completed!")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success rate: {(successful/(successful+failed))*100:.1f}%")


def main():
    print("Polish Dividend Data Scraper")
    print("=" * 40)

    scraper = PolishDividendScraper()
    scraper.scrape_all_companies()

    print("\nDone!")


if __name__ == "__main__":
    main()
