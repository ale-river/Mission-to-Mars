#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[4]:


time.sleep(4)

# Assign the HTML content of the page to a variable
news_html = browser.html

# Parse HTML with Beautifulsoup
soup = BeautifulSoup(news_html,'html.parser')


# In[5]:


# Retrieve the latest News Title and Paragraph Text
result = soup.find('div', class_="list_text")

news_title = result.a.text
news_p = result.find('div',class_="article_teaser_body").text

print(f"news_title: {news_title}")
print(f"news_p: {news_p}")


# ### JPL Space Images Featured Image

# In[6]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[7]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[8]:


# Parse the resulting html with soup
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')
img_soup


# In[9]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[10]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[11]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[12]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[13]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[14]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)


# In[15]:


time.sleep(4)

# Assign the HTML content of the page to a variable
hemisphere_html = browser.html
# Parse HTML with Beautifulsoup
soup = BeautifulSoup(hemisphere_html,'html.parser')


# In[16]:


# Collect the urls for the hemisphere images
items = soup.find_all("div", class_="item")

main_url = "https://astrogeology.usgs.gov"
hemisphere_urls = []

for item in items:
    hemisphere_urls.append(f"{main_url}{item.find('a', class_='itemLink')['href']}")

print(*hemisphere_urls, sep = "\n")


# In[17]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for url in hemisphere_urls:
    # Navigate to the page
    browser.visit(url)
    
    time.sleep(4)
    
    # Assign the HTML content of the page to a variable
    hemisphere_html = browser.html
    # Parse HTML with Beautifulsoup
    soup = BeautifulSoup(hemisphere_html,'html.parser')
    
    img_url = soup.find('img', class_="wide-image")['src']
    title = soup.find('h2', class_="title").text
    
    hemisphere_image_urls.append({"title":title,"img_url":f"https://astrogeology.usgs.gov{img_url}"})


# In[18]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[19]:


# 5. Quit the browser
browser.quit()


# In[ ]:




