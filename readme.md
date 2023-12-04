Biotech 10K data from kaggle https://www.kaggle.com/datasets/andersward/10k-statement-data-for-us-biotech-companies

From this data I extracted all of the symbols for use with multiple web scraping tools. 

Next I created yfSymbols.py to get every symbols name, sector, and industry from yahoo finance. 

I then created glassdoor.py and used the names from biotech_comps_saved.csv to individually scrape each companies salary data from glassdoor.com. Make sure when running glassdoor.py to change the username and password to your own glassdoor.com login. 

Then the data is merged to create a one csv of the name symbol, sector, industry, and avg_salary data from biotech_salaries.csv and another csv of the symbol and upperbound salary data for each job of each company from biotech_salaries.csv. The data was cleaned, merged, and saved in /Saved_Cleaned/final, using clean_and_merge.ipynb and final.ipynb.