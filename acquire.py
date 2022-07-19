# #getting the urls from a website
# def get_blog_articles():
#     url = 'https://codeup.com/blog/'
#     headers = {'User-Agent': 'Codeup News & Articles'} # Some websites don't accept the pyhon-requests default user-agent
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text)
#     urls = [a.attrs['href']for a in soup.select('a.more-link')]
#     return urls



# # url = 'https://codeup.com/workshops/in-person-workshop-learn-to-code-python-on-7-19/'
# # headers = {'User-Agent': '#post-18698 > div:nth-child(1) > h1'} # Some websites don't accept the pyhon-requests default user-agent
# # response = get(url, headers=headers)
# # soup = BeautifulSoup(response.content, 'html.parser')


# ######### always add the the code up here to make a the the code make sense. the headers are coppied from the 
# def parse_blog_article(soup):
#     return {
#         'title': soup.select_one('h1.entry-title').text,
#         'published': soup.select_one('.published').text,
#         'content': soup.select_one('.entry-content').text.strip(),
#     }

from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd

def get_blog_articles_data(refresh=False):
    
    if not os.path.isfile('blog_articles.csv') or refresh:
        
        url = 'https://codeup.com/blog/'
        headers = {'User-Agent': 'Codeup Data Science'}
        response = get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        links = [link['href'] for link in soup.select('h2 a[href]')]

        articles = []

        for url in links:

            url_response = get(url, headers=headers)
            soup = BeautifulSoup(url_response.text, 'html.parser')

            title = soup.find('h1', class_='entry-title').text
            content = soup.find('div', class_='entry-content').text.strip()

            article_dict = {
                'title': title,
                'content': content
            }

            articles.append(article_dict)
        
        blog_article_df = pd.DataFrame(articles)
        
        blog_article_df.to_csv('blog_articles.csv', index=False)
        
    return pd.read_csv('blog_articles.csv')

def get_news_articles_data(refresh=False):
    
    if not os.path.isfile('news_articles.csv') or refresh:
        
        url = 'https://inshorts.com/en/read'
        response = get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        categories = [li.text.lower() for li in soup.select('li')][1:]
        categories[0] = 'national'

        inshorts = []

        for category in categories:

            cat_url = url + '/' + category
            response = get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            titles = [span.text for span in soup.find_all('span', itemprop='headline')]
            contents = [div.text for div in soup.find_all('div', itemprop='articleBody')]

            for i in range(len(titles)):

                article = {
                    'title': titles[i],
                    'content': contents[i],
                    'category': category,
                }

                inshorts.append(article)
                
        inshorts_article_df = pd.DataFrame(inshorts)
        
        inshorts_article_df.to_csv('news_articles.csv', index=False)
                
    return pd.read_csv('news_articles.csv')