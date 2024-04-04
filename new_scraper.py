import requests
from bs4 import BeautifulSoup
from random import uniform
import json
import csv

# URL of the page to scrape
url = 'https://bedstebonusser.com/'
# Headers to mimic a web browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send a GET request to the URL with the headers
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

# List of section data-ids to target
section_ids = ['a03e393', '8f9bf16', '7b81df5', '5f4f447', 'a746244', '96baefa', 'a5fe24d', '1c4d4c3', '918b375', 'a49402c', 'a275d56', 'e99a5e9', '6e785e1']

data = []

for data_id in section_ids:
    # Generate a random score between 9.4 and 9.9, rounded to 1 decimal place
    random_score = round(uniform(9.4, 9.9), 1)

    section = soup.find('section', {"data-id": data_id})
    if not section:
        print(f"Section with data-id {data_id} not found")
        continue

    # Extract the necessary data
    img = section.find('img')
    img_url = img['src'] if img else 'No image found'

    paragraph = section.find('p')
    paragraph_text = paragraph.text if paragraph else 'No paragraph found'

    heading = section.find('h2')
    heading_bonus_text = heading.text if heading else 'No bonus found'

    data.append({
        'data_id': data_id,
        'bookmaker-thumbnail': img_url,
        'rules': paragraph_text,
        'bonus': heading_bonus_text,
        'affiliate_link': 'insert affiliate link here',
        'score': random_score
    })

# Convert to JSON and save
json_data = json.dumps(data, indent=4, ensure_ascii=False)
with open('data.json', 'w', encoding='utf-8') as file:
    file.write(json_data)

# Save data to CSV
csv_columns = ['data_id', 'img_url', 'rules', 'bonus', 'affiliate_link', 'score']
csv_file = "data.csv"
try:
    with open(csv_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
except IOError:
    print("I/O error")

print("Data saved to JSON and CSV.")
