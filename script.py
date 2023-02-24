import requests
from bs4 import BeautifulSoup
import csv

url = 'https://awards.acm.org/award-recipients'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with class "awards-tables--fullWidth"
table = soup.find('table', {'class': 'awards-tables--fullWidth'})

# Find all the rows in the table body
rows = table.find('tbody').find_all('tr')

# Create a list to store the scraped data
data = []

# Loop through each row and extract the name, award, year, region, and DL link
for row in rows:
    name = row.find('a').text.strip()
    award = row.find_all('a')[1].text.strip()
    year = row.find('td', {'role': 'rowheader'}).text.strip()
    region = row.find_all('td')[1].text.strip()
    dl = row.find('td', {'class': 'dl-logo'})
    if dl and dl.find('a', href=True):
        dl_link = dl.find('a')['href']
    else:
        dl_link = ''
    data.append([name, award, year, region, dl_link])

# Save the data to a CSV file
with open('acm_award_recipients.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Award', 'Year', 'Region', 'DL'])
    writer.writerows(data)

# Loop through the data and extract the slideshow data
for row in data:
    name = row[0]
    dl_link = row[4]
    if dl_link:
        response = requests.get(dl_link)
        soup = BeautifulSoup(response.content, 'html.parser')
        slideshow = soup.find('div', {'class': 'slideShow'})
        if slideshow:
            rows = []
            for slide in slideshow.find_all('div', {'class': 'slide-item'}):
                title_elem = slide.find('div', {'class': 'bibliometrics__title'})
                if title_elem:
                    title = title_elem.text.strip()
                else:
                    title = 'N/A'  
                # Find the bibliometrics__count element and get its text value
                value_elem = slide.find('div', {'class': 'bibliometrics__count'})
                if value_elem is not None:
                    value = value_elem.text.strip()
                else:
                    value = ""

                rows.append([name, title, value])
            with open('slideshow.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name ACM Award Recipients', 'Title', 'Value'])
                writer.writerows(rows)
