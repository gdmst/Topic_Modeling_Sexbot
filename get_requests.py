import requests
from bs4 import BeautifulSoup

# Making a GET request
headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"
            }
url = 'https://dl.acm.org/doi/abs/10.1145/3184558.3188730'

r = requests.get(url, headers=headers)
# check status code for response received
# success code - 200

# print content of request
print(r)
soup = BeautifulSoup(r.content, 'html.parser')
print(soup.prettify())