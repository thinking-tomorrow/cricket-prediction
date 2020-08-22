from bs4 import BeautifulSoup
import requests

source = requests.get("https://www.icccricketschedule.com/vivo-ipl-2020-schedule-team-venue-time-table-pdf-point-table-ranking-winning-prediction/").text
soup = BeautifulSoup(source,'lxml')

table = soup.find('tr')

print(table)