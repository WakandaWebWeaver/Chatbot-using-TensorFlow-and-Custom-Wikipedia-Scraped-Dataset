import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

def get_text_from_wikipedia_page(title):
    base_url = 'https://en.wikipedia.org/wiki/'
    url = base_url + title.replace(' ', '_')
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    
    return text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n', ' ', text)
    return text.strip()

def save_text_to_file(text, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(text)

articles_to_scrape = [
    'Effective_Communication',
    'Common_Idioms_and_Expressions',
    'Social_and_Cultural_Norms',
    'Classic_Literature_Extracts',
    'Speechwriting_and_Rhetoric',
    'Grammar_and_Syntax_Guides',
    'Creative_Writing_Techniques',
    'Famous_Speech_Transcripts',
    'Interview_Transcripts',
    'TED_Talks_Transcripts'
]
output_directory = 'scraped_data/'

for article in tqdm(articles_to_scrape, desc='Scraping Wikipedia'):
    text = get_text_from_wikipedia_page(article)
    cleaned_text = clean_text(text)
    
    save_text_to_file(cleaned_text, 'data.txt')

print("Scraping, saving done.")
