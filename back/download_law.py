import requests
import urllib.parse
from bs4 import BeautifulSoup

def get_legislation_content(title):
    encoded_title = urllib.parse.quote(title)
    url = f"http://www.legislation.gov.uk/id?title={encoded_title}"
    response = requests.get(url)
    
    if response.status_code == 301:
        canonical_url = response.headers['Location']
        print(f"Canonical URI: {canonical_url}")
    elif response.status_code == 303:
        print("Multiple choices found:")
        print(response.text)
    elif response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        body_tag = soup.find('body', attrs={'about': True})
        
        if body_tag:
            legislation_url = body_tag['about'][:-13] + 'made?view=plain'
            return extract_content_text(legislation_url)
        else:
            print("No 'about' attribute found in <body> tag.")
    else:
        print(f"Error: Received status code {response.status_code}")

def extract_content_text(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', id='content')
        
        if content_div:
            return content_div.get_text(strip=True)
        else:
            print("No <div> with id 'content' found.")
    else:
        print(f"Error: Received status code {response.status_code}")

# # Example usage
# title = "Criminal Justice Bill Report Stage"
# content_text = get_legislation_content(title)
# print(content_text)
