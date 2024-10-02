from GoogleNews import GoogleNews
import pandas as pd
from pathlib import Path  

googlenews = GoogleNews()

for year in range(2010, 2025):
    print(year)

    start_date = '01/01/'+str(year)
    end_date = '12/31/'+str(year)
    googlenews=GoogleNews(start=start_date,end=end_date)
    googlenews.search('sex robot')
    googlenews.set_encode('utf-8')
    googlenews.get_news('sex robot')

    result=googlenews.result()
    df=pd.DataFrame(result)
    
    # for i in range(2,20):
    #     googlenews.getpage(i)
    #     result=googlenews.result()
    #     df=pd.DataFrame(result)

    filepath_allnews = Path('results/sex_robot_links_'+str(year)+'.csv')   #todo: change file name
    filepath_allnews.parent.mkdir(parents=True, exist_ok=True)  
    df.to_csv(filepath_allnews) 

     