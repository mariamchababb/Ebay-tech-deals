# Web-Scraping-Automation-2

## eBay Tech Deals Data Pipeline

## Overview

This project builds a complete data pipeline that scrapes, processes, and analyzes technology deals from the eBay Global Tech Deals page.

The pipeline automatically collects product data over time, cleans and organizes the dataset, and performs exploratory data analysis (EDA) to uncover trends in pricing, discounts, and shipping options.

## Methodology

### 1. Web Scraping

A Selenium-based scraper (`scraper.py`) was developed to gather product information from the eBay Global Tech Deals page.

The scraper collects the following fields:

- timestamp
- title
- price
- original_price
- shipping
- item_url

To capture all available listings, the scraper scrolls through the page to trigger lazy loading and load additional product tiles.

The collected data is appended to: [ebay_tech_deals.csv](./ebay_tech_deals.csv)

### 2. Automation with GitHub Actions

The scraper is automated using GitHub Actions and runs every **3 hours**.

Cron schedule used: `0 */3 * * *`

Each execution gathers new deal data and appends it to the dataset, gradually building a time-based dataset over roughly two days.

### 3. Data Cleaning

The script `clean_data.py` processes the raw scraped data by:

- Removing `US $` symbols and commas from price fields
- Converting price values into numeric format
- Handling missing `original_price` values
- Cleaning missing shipping information
- Creating a new feature called `discount_percentage`

The cleaned dataset is saved as: [cleaned_ebay_deals.csv](./cleaned_ebay_deals.csv)

### 4. Exploratory Data Analysis

Exploratory data analysis was conducted in the notebook: [EDA.ipynb](./EDA.ipynb)

The analysis includes:

- Time series analysis of deals scraped per hour
- Distribution of product prices
- Comparison between original and discounted prices
- Discount percentage distribution
- Frequency of different shipping options
- Keyword analysis in product titles
- Price difference analysis
- Identification of the top 5 highest discounts

All visualizations were created using **Matplotlib** and **Seaborn**.

## Key Findings

Some general insights from the analysis include:

- Most deals fall within a specific price range.
- Several products show noticeable discounts compared to their original prices.
- Certain brands and keywords, such as Apple and Samsung, appear frequently in the dataset.
- Free shipping is the most common shipping option across the deals.

## Challenges Faced

Several technical challenges were encountered during the project:

- The page loads content dynamically, requiring scrolling to ensure all products are loaded.
- Selenium occasionally returned a slightly different page structure compared to a regular browser session.
- Some product tiles initially lacked certain fields (such as title or price), which required additional validation logic.

## Potential Improvements

Possible future improvements include:

- Removing duplicate products across multiple scraping runs
- Collecting additional product details such as ratings or number of reviews
- Running the scraper o
ver a longer time period to analyze pricing trends
- Using an API-based approach (if available) to improve reliability
 