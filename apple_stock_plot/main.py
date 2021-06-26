from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(4)

driver.get('https://in.finance.yahoo.com/quote/AAPL?ltr=1')
driver.maximize_window()

driver.find_element(by = By.XPATH, value = '//*[@id="quote-nav"]/ul/li[5]/a').click()
driver.find_element(by = By.XPATH, value = '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a').click()

apple = pd.read_csv('/content/AAPL.csv')
apple["percentage_change"] = np.nan

index = 5

for i in range(1, len(apple)) :
    value = ((apple['Adj Close'][i] - apple['Adj Close'][i-1])/apple['Adj Close'][i-1])*100
    apple['percentage_change'][i] = value

apple['Adj Close'].plot()
plt.xlabel("Date")
plt.ylabel("Adjusted")
plt.title("Apple Price data")
plt.show()

apple_daily_returns = apple['Adj Close'].pct_change()

fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.plot(apple_daily_returns)
ax1.set_xlabel("Date")
ax1.set_ylabel("Percent")
ax1.set_title("Apple daily returns data")
plt.show()

fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
apple_daily_returns.plot.hist(bins = 60)
ax1.set_xlabel("Daily returns %")
ax1.set_ylabel("Percent")
ax1.set_title("Apple daily returns data")
plt.show()

apple_cum_returns = (apple_daily_returns + 1).cumprod()

fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
apple_cum_returns.plot()
ax1.set_xlabel("Date")
ax1.set_ylabel("Growth of $1 investment")
ax1.set_title("Apple daily cumulative returns data")
plt.show()
