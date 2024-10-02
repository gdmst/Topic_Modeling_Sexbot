# to download all the article from news.csv 

import csv
from newspaper import Article
import pandas as pd
from pathlib import Path  
from newspaper import Config
import nltk
import requests
from selenium import webdriver



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

def download_article(df, path_name):

    list=[]
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent

    # for ind in df.index:
    ind = 0
    article = Article(df['link'][ind],config=config)

    print("downloading article from:" + df['link'][ind])

    try:
        article.download()
        article.parse()
        article.nlp()
        dict={}
        dict['Date']=df['date'][ind]
        dict['Media']=df['media'][ind]
        dict['Title']=article.title
        dict['Article']=article.text
        dict['Summary']=article.summary
        print(dict['Summary'])
        list.append(dict)   
    except:
        print("cannot download" + df['link'][ind])

        

    news_df=pd.DataFrame(list)
    filepath = Path(path_name)  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    news_df.to_csv(filepath) 

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

if __name__ == "__main__":
    file_path = 'results/sex_robot_news_all.csv'  # Replace with your CSV file path
    csv_data = read_csv(file_path)
    
    df_news = pd.DataFrame(csv_data)
    # convert_links(df_news)

    download_article(df_news, "results/sex_robot_article_2.csv")