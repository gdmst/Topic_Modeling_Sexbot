# to download all the article from news.csv 

import csv
from newspaper import Article
import pandas as pd
from pathlib import Path  
from newspaper import Config
import nltk
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

def download_article(df):

    list=[]

    for ind in df.index:

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
    filepath = Path('results/Sexbot_Articles_2.csv')  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    news_df.to_csv(filepath) 


# Example usage
if __name__ == "__main__":
    file_path = 'data.csv'  # Replace with your CSV file path
    csv_data = read_csv(file_path)
    print(csv_data)
