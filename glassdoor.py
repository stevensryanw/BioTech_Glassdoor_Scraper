#Scrape https://www.glassdoor.com for salaries of each symbol in biotech.csv
#Ryan Stevens

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import random
import csv

#Read in all companies from biotech_comps.csv
comps = pd.read_csv('biotech_comps_saved.csv')
names = comps['name'].unique()
symbols = comps['symbol'].unique()

CompSals = []
PosSals = []

sals = pd.read_csv('biotech_salaries_clean.csv') #list of companies and average salaries
Psals = pd.read_csv('biotech_positions_clean.csv') #list of positions and upper bound salaries

# Combine the previously scraped data into new arrays
for name in names[len(CompSals):]:
    comp_salary = sals.loc[sals['Company'] == name, 'Average Salary'].values
    if len(comp_salary) > 0:
        CompSals.append([name, comp_salary[0]])

    pos_salaries = Psals.loc[Psals['Company'] == name]
    if not pos_salaries.empty:
        positions = pos_salaries['Position'].values
        salaries = pos_salaries['Salary'].values
        for position, salary in zip(positions, salaries):
            PosSals.append([name, position, salary])

def randLoginNum():
    return random.randint(3, 10)

def randSleepNum():
    return random.randint(10, 40)

#path = '/Users/ryanstevens/Desktop/Service Learning (MGMT4600)/chromedriver'
driver = webdriver.Chrome()
#driver.maximize_window()

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
#opts.add_argument("--headless")

#Open glassdoor.com
url = 'https://www.glassdoor.com'
for i in range(100):
    biotech_salaries = pd.read_csv('biotech_salaries.csv')
    biotech_comps = pd.read_csv('biotech_comps_saved.csv')

    #Lets figure out which how many companies havent had their salaries posted or pages that are scrapable
    #To do this lets compare the so far scraped salaries with all companies in biotech_comps_saved
    namesScraped = biotech_salaries['Company'].tolist()
    namesTotal = biotech_comps['name'].tolist()

    #Lets see which companies have not had their salaries scraped
    namesNotScraped = []
    for name in namesTotal:
        if name == namesScraped[-1]:
            break
        if name not in namesScraped:
            namesNotScraped.append(name)

    cite_fail = 0
    fail = len(namesNotScraped)
    try:
        driver.get(url)
        time.sleep(randLoginNum())
        #Login to glassdoor.com
        user = 'your_user'
        password = 'your_pass'

        #Email text input XPATH: //*[@id="inlineUserEmail"]
        email_text = driver.find_element('xpath', '//*[@id="inlineUserEmail"]')
        email_text.send_keys(user)
        time.sleep(randLoginNum())
        #Click continue button XPATH: //*[@id="InlineLoginModule"]/div/div/div[1]/div/div/div/div/form/div[2]/button
        continue_button = driver.find_element('xpath', '//*[@id="InlineLoginModule"]/div/div/div[1]/div/div/div/div/form/div[2]/button')
        continue_button.click()
        time.sleep(randLoginNum())
        #Password text input XPATH: //*[@id="inlineUserPassword"]
        password_text = driver.find_element('xpath', '//*[@id="inlineUserPassword"]')
        password_text.send_keys(password)
        time.sleep(randLoginNum())
        # Click sign in button XPATH: //*[@id="InlineLoginModule"]/div/div/div[1]/div/div/div/div/form/div[2]/button
        signin_button = driver.find_element('xpath', '//*[@id="InlineLoginModule"]/div/div/div[1]/div/div/div/div/form/div[2]/button')
        signin_button.click()
        time.sleep(randLoginNum())

        # Lets start where we left off and for testing only 3 companies
        for name in names[len(CompSals)+fail:]:
            print(name)
            # Search for symbol
            try:
                # Click search bar XPATH: /html/body/header/div/div/div[3]/div[1]/button
                search_bar = driver.find_element('xpath', '/html/body/header/div/div/div[3]/div[1]/button')
                search_bar.click()
                time.sleep(randLoginNum())
                search_bar.send_keys(name+Keys.ENTER)
                time.sleep(randLoginNum())
                # Click on the result XPATH: //*[@id="Discover"]/div/div/div[1]/div[1]/div
                result = driver.find_element('xpath', '//*[@id="Discover"]/div/div/div[1]/div[1]/div')
                result.click()
                time.sleep(randLoginNum())
                # Click the salaries tab XPATH: //*[@id="EmpLinksWrapper"]/div[2]/div/div[1]/a[3]
                salaries_tab = driver.find_element('xpath', '//*[@id="EmpLinksWrapper"]/div[2]/div/div[1]/a[3]')
                salaries_tab.click()
                time.sleep(randLoginNum())
            except:
                # Go back to home page XPATH: //*[@id="globalNavContainer"]/div/div[1]
                fail += 1
                print('Failed to find', fail)
                home_button = driver.find_element('xpath', '//*[@id="globalNavContainer"]/div/div[1]')
                home_button.click()
                time.sleep(randLoginNum())
                continue

            # Find the table element on the page
            # Lets make it so that if there is no table then we skip this symbol
            try:
                table = driver.find_element('xpath', '//*[@id="__next"]/div/main/section[2]/table/tbody')
                time.sleep(randLoginNum())
                salaries = []
                # Iterate through the table rows starting from row 1
                rows = table.find_elements(By.TAG_NAME, 'tr')
                for row in rows[1:]:
                    # Get the upper bound of the salary range
                    salary_range = row.find_elements(By.TAG_NAME, 'td')[1].text.split('\n')[0]
                    upper_bound = salary_range.split('-')[1]
                    # We need to remove the $ and K from the upper bound to convert it to an int
                    upper_bound = upper_bound.replace('$', '')
                    upper_bound = upper_bound.replace('K', '')
                    upper_bound = int(upper_bound)
                    # Get the job type
                    job_type = row.find_elements(By.TAG_NAME, 'td')[0].text

                    # Add the upper bound to the salaries list
                    salaries.append(upper_bound)
                    PosSals.append([name, job_type, upper_bound])

                # Calculate the average salary
                average_salary = sum(salaries)/len(salaries)
                #print(average_salary)
                CompSals.append([name, average_salary])
                print(CompSals)
                #print(len(CompSals))
            except:
                continue

            time.sleep(randSleepNum())

            # Alternatively, you can use pandas to write the data to CSV files
            dfSals = pd.DataFrame(CompSals, columns=['Company', 'Average Salary'])
            dfSals.to_csv('biotech_salaries.csv', index=False)

            dfPos = pd.DataFrame(PosSals, columns=['Company', 'Position', 'Salary'])
            dfPos.to_csv('biotech_positions.csv', index=False)

            # Go back to home page XPATH: //*[@id="globalNavContainer"]/div/div[1]
            home_button = driver.find_element('xpath', '//*[@id="globalNavContainer"]/div/div[1]')
            home_button.click()
            time.sleep(randLoginNum())
    except:
        cite_fail += 1
        print('Failed to find', cite_fail)
        time.sleep(randSleepNum())
        continue