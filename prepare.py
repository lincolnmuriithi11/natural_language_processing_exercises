
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup


import pandas as pd

import acquire

#function that cleans a string 
def basic_clean(string):
    """basic_clean. It should take in a string and apply some basic text cleaning to it:

        Lowercase everything
        Normalize unicode characters
        Replace anything that is not a letter, number, whitespace or a single quote."""
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    string = re.sub(r'[^a-z0-9\'\s]', '', string).lower()
    return string

def tokenize(string):
    """tokenize. It should take in a string and tokenize all the words in the string."""
    tokenizer = nltk.tokenize.ToktokTokenizer()
    string = tokenizer.tokenize(string, return_str=True)
    return tokenizer.tokenize(string, return_str=True)

def stem(string):
    """It should accept some text and return the text after applying stemming to all the words."""
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    return ' '.join(stems)

def lemmatize(string):
    """It should accept some text and return the text after applying lemmatization to each word."""
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    return ' '.join(lemmas)

def remove_stopwords(string, extra_words = None, exclude_words = None):
    """ It should accept some text and return the text after removing all 
    the stopwords. This function should define two optional parameters, 
    extra_words and exclude_words. These parameters should define any additional 
    stop words to include, and any words that we don't want to remove."""
    stopword_list = stopwords.words('english')
    if extra_words != None:
        stopword_list = stopword_list.append(extrawords)
    if exclude_words != None:
        stopword_list = stopword_list.remove(exclude_words)
    words = string.split()
    filtered_words = [w for w in words if w not in stopword_list]
    return ' '.join(filtered_words)

def news_df_prepare(df,column,extra_words=[],exclude_words=[]):
    df.rename({'content':'original'}, axis=1, inplace=True)
    df['clean'] = df.original.apply(basic_clean)
    df['clean'] = df.clean.apply(tokenize)
    df['clean'] = df.clean.apply(remove_stopwords)
    df['stemmed'] = df.clean.apply(stem)
    df['lemmatized'] = df.clean.apply(lemmatize)
    return df[["title",column,"clean","stemmed","lemmatized"]]

def codeup_df_prepare():
    codeup_df = acquire.get_blog_articles_data(refresh=False)
    codeup_df.drop(columns= ['date','link'], inplace=True)
    codeup_df.rename({'content':'original'}, axis=1, inplace=True)
    codeup_df['clean'] = codeup_df.original.apply(basic_clean)
    codeup_df['clean'] = codeup_df.clean.apply(tokenize)
    codeup_df['clean'] = codeup_df.clean.apply(remove_stopwords)
    codeup_df['stemmed'] = codeup_df.clean.apply(stem)
    codeup_df['lemmatized'] = codeup_df.clean.apply(lemmatize)
    return codeup_df