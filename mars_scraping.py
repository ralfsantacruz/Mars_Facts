from bs4 import BeautifulSoup as bs
from splinter import Browser
from pprint import pprint
import random as r

import re
import pandas as pd


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

def get_soup(url):
    """ 
    This function uses splinter and beautiful soup to serve you up a BeautifulSoup object to scrape from.
        Just hit it with your url of interest and you're all set.
        
    """

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    return soup   


# In[4]:


def text(x):
    """ 
    Deletes all '\n' instances in HTML text to clean it up. Requires a parsed BeautifulSoup object.
    """
    return x.text.replace('\n','')


# In[5]:


def random_element(x):
    """
    Takes in a list and returns a random element from the list.
    If there's only one element, return first element.
    """
    if len(x) > 1:
        return x[r.randint(0,len(x)-1)]
    else:
        return x[0]


# In[6]:


# Scrape the Mars news website.
def mars_headlines():
    """
    Returns a list of dictionaries for the Mars News headlines and their descriptions.
    """
    mars_news = get_soup("https://mars.nasa.gov/news/")
    # Find headlines and descriptions
    headlines = mars_news.find_all('div',class_="content_title")
    descriptions =  mars_news.find_all('div',class_="article_teaser_body")
    # Make a list of dictionaries for every headline and its description.
    mars_headlines = [{'title': text(a), 'description': text(b)} for a,b, in zip(headlines,descriptions)]
    return mars_headlines


# In[7]:


# Scrape the JPL Images site.
def featured_image():
    """ 
    Returns the featured image url on the JPL.nasa.gov website
    """
    JPL = get_soup("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit")
    # Finds url path for the full-res featured image on the JPL gallery and concatenates it to form proper url.
    css_styling = JPL.find('article', class_="carousel_item")['style']
    string = css_styling.split()[1]
    result = re.search("'(.*)'", string)
    featured_url = result.group(1)
    return "https://www.jpl.nasa.gov" + featured_url


# In[8]:


# Scrape the Mars Twitter Website
def get_tweets():
    """
    Returns a list of tweets from Mars weather Twitter page.
    Only returns tweets that have been loaded upon navigation to the page.
    """
    mars_twitter = get_soup("https://twitter.com/marswxreport?lang=en")
    tweets = mars_twitter.find_all('div', class_="js-tweet-text-container")
    tweet_list = [text(tweet) for tweet in tweets]
        
    return tweet_list


# In[9]:


# Scrape the Mars Facts site to extract the planet profile table and clean it up.
def mars_html_table():
    """ 
    Returns the the Mars planet profile as an html table
    """
    mars_facts = pd.read_html("https://space-facts.com/mars/")[0]
    mars_facts.columns=['Mars Profile','']
    mars_facts = mars_facts.set_index('Mars Profile')
    # Export the table to HTML
    mars_table = mars_facts.to_html(escape=False)
    return mars_table


# In[10]:


# Scrapes USGS website to obtain a list of urls for pictures of the 4 hemispheres of Mars.
def mars_hemispheres():  
    """ 
    Returns a list of dictionarties containing image urls and their titles for the 4 hemispheres of Mars.
    """
    pic_list = []
    parent_url = "https://astrogeology.usgs.gov"
    
    USGS = get_soup("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

    # Duplicate links are avoided by slicing the list to return every odd element. '[1::2]'
    # Cannot scrape names from even elements in list.
    hemisphere_url_paths = USGS.find_all(class_="itemLink product-item")[1::2]
    
    hemisphere_names = [name.text.replace(' Enhanced','') for name in hemisphere_url_paths]
    hemisphere_links = [parent_url + path['href'] for path in hemisphere_url_paths]
    
    # Goes through each link and scrapes the image url for the given hemisphere
    for link in hemisphere_links:
        pic_url = get_soup(link).find('div', class_='downloads').find('a')['href']
        pic_list.append(pic_url)
    
    url_dictionary = [{'title': a, 'img_url': b} for a,b in zip(hemisphere_names,pic_list)]
    
    return url_dictionary


# In[11]:


def scrape():
    dic = {}
    dic['headlines'] = random_element(mars_headlines())
    dic['featured_image'] = featured_image()
    dic['tweets'] = random_element(get_tweets())
    dic['fact_table'] = mars_html_table()
    dic['hemispheres'] = mars_hemispheres()
    return dic

