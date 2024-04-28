import json
import requests
import time
from bs4 import BeautifulSoup


URL = 'http://quotes.toscrape.com'

def main():
    quotes = []
    authors = []
    next_page = True
    page_num = 1
    
    while next_page:
        data = requests.get(f'{URL}/page/{page_num}/')
        
        if data.status_code == 200:
            soup = BeautifulSoup(data.content, 'html.parser')
            data_quotes = soup.find_all('div', class_='quote')
            
            for item in data_quotes:
                quote = item.find('span', class_='text').text
                author = item.find('small', class_='author').text
                author_link = item.find('a')['href']
                tags = item.find_all('a', class_='tag')
                tags_list = []
                
                for tag in tags:
                    tags_list.append(tag.text)
                
                quote_dict = {'tags': tags_list,
                            'author': author,
                            'quote': quote}
                quotes.append(quote_dict)
                
                if author_link:
                    author_data = requests.get(URL + author_link)
                    
                    if author_data.status_code == 200:
                        soup = BeautifulSoup(author_data.content, 'html.parser')
                        author = soup.find('h3', class_='author-title').text
                        born_date = soup.find('span', class_='author-born-date').text
                        born_location = soup.find('span', class_='author-born-location').text
                        description = soup.find('div', class_='author-description').text.strip()
                        author_dict = {'fullname': author,
                                'born_date': born_date,
                                'born_location': born_location,
                                'description': description}
                        authors.append(author_dict)

            if soup.find('li', class_='next'):
                page_num += 1
                time.sleep(1)
            else:
                break
    return quotes, authors

if __name__ == '__main__':
    quotes, authors = main()

    with open('quotes.json', 'w', encoding='utf-8') as file:
        json.dump(quotes, file, indent='\t')

    with open('authors.json', 'w', encoding='utf-8') as fi:
        json.dump(authors, fi, indent=4)
