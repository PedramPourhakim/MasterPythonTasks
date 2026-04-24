import csv

import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.mehrnews.com/')
soup = BeautifulSoup(response.content, 'html.parser')

news_items = soup.find_all('li',class_="news")

output_file = open("output.csv","w",newline="",encoding="utf-8")
output_writer = csv.writer(output_file,delimiter=",")

output_writer.writerow(["Title","Link"])

for item in news_items:
    link = item.find('a')
    if link:
        title = link.get_text(strip=True)
        href = link.get('href')
        output_writer.writerow([title,href])