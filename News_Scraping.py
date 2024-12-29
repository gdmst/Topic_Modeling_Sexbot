# to download all the article from news.csv 

import csv
from newspaper import Article
import pandas as pd
from pathlib import Path  
from newspaper import Config
import nltk
import requests
from selenium import webdriver

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random





from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
#config will allow us to access the specified url for which we are #not authorized. Sometimes we may get 403 client error while parsing #the link to download the article.
nltk.download('punkt_tab')
nltk.download('punkt')

def read_csv(file_path):

    data = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return data

def parse_article(news_link, news_date, news_media, html_source, path_name):

    list=[]
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent

    # for ind in df.index:
    ind = 0
    article = Article(news_link, config=config)

    # print("downloading article from:" + news_link)

    try:
        article.download(input_html=html_source)
        article.parse()
        article.nlp()
        dict={}
        dict['Date']=news_date
        dict['Media']=news_media
        dict['Title']=article.title
        dict['Article']=article.text
        dict['Summary']=article.summary
        # print(dict['Summary'])
        list.append(dict)   
    except:
        print("cannot download" + news_link)


    news_df=pd.DataFrame(list)
    filepath = Path(path_name)  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    news_df.to_csv(filepath, mode='a', index=False, header=False)      

    print("parse news succesfully")

def convert_links(df):
    # for ind in df.index:
    
    
    options = webdriver.FirefoxOptions()
    options.add_argument('ignore-certificate-errors')
    driver = webdriver.Firefox(options=options)
    driver.get(df['link'][1])
    print(driver.current_url)
    # path_name = 'results/sex_robot_news_all.csv'
    # filepath = Path(path_name)  
    # filepath.parent.mkdir(parents=True, exist_ok=True)  
    # df.to_csv(filepath) 

def download_website(link):
    html_result = ""


    try:
        # Go to the initial URL
        driver.get(link)
        
        pause = random.randint(6,10)
        time.sleep(pause)  
        
        # Get the current URL and page source after redirection
        final_url = driver.current_url
        page_source = driver.page_source
        
        # print("Final URL:", link)
        html_result = page_source
    finally:
        print('successfully downloaded')

    
    return html_result

if __name__ == "__main__":
    service = Service(executable_path='/Users/uraiwanjansong/Research/Topic_Modeling/.venv/bin/geckodriver')
    driver = webdriver.Firefox(service=service)
    for year in range(2010,2014):
        file_path = 'results/sex_bot/sex_robot_'+str(year)+'.csv'  # Replace with your CSV file path
        csv_data = read_csv(file_path)
        
        df_news = pd.DataFrame(csv_data)
        # convert_links(df_news)

        for ind in df_news.index:
        # for ind in range(0,1):
            print('year '+ str(year) +' round: ', ind)
            html_source = download_website(df_news['link'][ind])
            # print(html_source)
            parse_article(df_news['link'][ind], 
                        df_news['date'][ind], 
                        df_news['media'][ind], 
                        html_source, 
                        'results/article/sex_bot/sex_bot_article_'+str(year)+'.csv')
    driver.quit()
        