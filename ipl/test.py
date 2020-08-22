from bs4 import BeautifulSoup
import requests

source = requests.get("https://www.icccricketschedule.com/vivo-ipl-2020-schedule-team-venue-time-table-pdf-point-table-ranking-winning-prediction/").text
soup = BeautifulSoup(source,'lxml')

table = soup.find('table')

'''for matches in table:

    rows = matches.find_all('td')
    print(rows[1])'''

matches_rows = table.find_all('tr')
matches_rows=matches_rows[1:]

for matches in matches_rows:

    new = matches.find_all('td')
    new = list(map(lambda x:str(x.text).replace(',', ''), new))
    print(new[0])