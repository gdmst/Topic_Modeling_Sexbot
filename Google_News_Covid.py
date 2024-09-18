from GoogleNews import GoogleNews
from newspaper import Article
import pandas as pd
from pathlib import Path  

googlenews = GoogleNews()

# print(googlenews.getVersion())

googlenews=GoogleNews(start='05/01/2020',end='05/31/2020')
googlenews.search('Coronavirus')
result=googlenews.result()
df=pd.DataFrame(result)
# print(df.head())

for i in range(2,20):
    googlenews.getpage(i)
    result=googlenews.result()
    df=pd.DataFrame(result)


filepath = Path('results/covid.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)  