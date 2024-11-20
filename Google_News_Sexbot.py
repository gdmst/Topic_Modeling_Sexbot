from GoogleNews import GoogleNews
import pandas as pd
from pathlib import Path  
import calendar

googlenews = GoogleNews()

for year in range(2010, 2011):
    
    print(year)
    filepath_allnews = Path('results/sex_robot/sex_robot_'+str(year)+'.csv')   #todo: change file name
    filepath_allnews.parent.mkdir(parents=True, exist_ok=True)  

    for month in range(1,13): 
        
        start_date = str(month).zfill(2) + '/01/' + str(year)
        end_day = calendar.monthrange(year, month)[1]
        end_date = str(month).zfill(2) +'/'+ str(end_day) +'/'+str(year)
        print(start_date+ " - " + end_date)
        googlenews=GoogleNews(start=start_date,end=end_date)
        # googlenews.search('sex robot')
        googlenews.set_encode('utf-8')
        googlenews.get_news('sex robot')

        result=googlenews.result()
        df=pd.DataFrame(result)
        
        # for i in range(2,20):
        #     googlenews.getpage(i)
        #     result=googlenews.result()
        #     df=pd.DataFrame(result)

        
        df.to_csv(filepath_allnews, mode='a', index=False, header=False)         

     