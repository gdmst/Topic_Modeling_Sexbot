from GoogleNews import GoogleNews
from newspaper import Article
import pandas as pd
from pathlib import Path  
from newspaper import Config
import nltk
#config will allow us to access the specified url for which we are #not authorized. Sometimes we may get 403 client error while parsing #the link to download the article.
nltk.download('punkt_tab')
nltk.download('punkt')

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

googlenews = GoogleNews()

# print(googlenews.getVersion())

# googlenews=GoogleNews(start='05/01/2020',end='05/31/2020')
googlenews.search('Sexbot')
result=googlenews.result()
df=pd.DataFrame(result)
# print(df.head())

for i in range(2,20):
    googlenews.getpage(i)
    result=googlenews.result()
    df=pd.DataFrame(result)

filepath_allnews = Path('results/Sexbot_news.csv')  
filepath_allnews.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath_allnews) 

# filepath = Path('results/Sexbot.csv')  
# filepath.parent.mkdir(parents=True, exist_ok=True)  
# df.to_csv(filepath)  

list=[]
# for ind in df.index:
#     dict={}
#     article = Article(df['link'][ind],config=config)

#     #  todo add error handeling to catch and throw error in case we cannot download the article
#     try:
#         print("downloading article from: " + df['link'])
#         article.download()
#     except:
#         print("An ArticleException occurred: cannot downlaod article.")
    
#     article.parse()
#     article.nlp()
#     dict['Date']=df['date'][ind]
#     dict['Media']=df['media'][ind]
#     dict['Title']=article.title
#     dict['Article']=article.text
#     dict['Summary']=article.summary
#     print(dict['Summary'])
#     list.append(dict)

# for ind in df.index:

#     article = Article(df['link'][ind],config=config)

#     print("downloading article from:" + df['link'][ind])

#     try:
#         article.download()
#         article.parse()
#         article.nlp()
#         dict={}
#         dict['Date']=df['date'][ind]
#         dict['Media']=df['media'][ind]
#         dict['Title']=article.title
#         dict['Article']=article.text
#         dict['Summary']=article.summary
#         print(dict['Summary'])
#         list.append(dict)   
#     except:
#         print("cannot download" + df['link'][ind])

     

# news_df=pd.DataFrame(list)
# filepath = Path('results/Sexbot.csv')  
# filepath.parent.mkdir(parents=True, exist_ok=True)  
# news_df.to_csv(filepath) 
