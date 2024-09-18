from GoogleNews import GoogleNews
from newspaper import Article
import pandas as pd

googlenews = GoogleNews()

# print(googlenews.getVersion())

googlenews.set_lang('en')
# googlenews.set_period('7d')
# googlenews.set_time_range('02/01/2020','02/28/2020')
googlenews.set_encode('utf-8')

googlenews.get_news('APPLE')

# print(googlenews.results())

print(googlenews.get_links())