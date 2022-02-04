#!/usr/bin/env python
# coding: utf-8


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the resulting html with soup
html = browser.html
soup2 = soup(html, 'html.parser')

# Retrieve the parent divs for all articles
#results = soup2.find_all('div', class_='collapsible results')
results = soup2.find_all('div', class_='description')

hemisphere={}
title=[]
image_url=[]
scrape_url_list=[]

# loop over results to get title data
for i in results:
    #scrape the title
    scrape_title = i.find('a',class_="itemLink product-item")
    title_name=scrape_title.find("h3").text
    title.append(title_name)
    hemisphere["title"] = title
    scrape_click_link = i.a['href']
    scrape_url=url+scrape_click_link
    scrape_url_list.append(scrape_url)

# print(title)
# print(scrape_url_list)

scrape_url_1=scrape_url_list[0]
scrape_url_2=scrape_url_list[1]
scrape_url_3=scrape_url_list[2]
scrape_url_4=scrape_url_list[3]
# print(scrape_url_1)
# print(scrape_url_2)
# print(scrape_url_3)
# print(scrape_url_4)


browser.visit(scrape_url_1)    
html1 = browser.html
soup3 = soup(html1, 'html.parser')
results1 = soup3.find_all('li')[0]
# print(results1)
url1=results1.a['href']
title_url1=url+url1
# print(title_url1)


browser.visit(scrape_url_2)    
html2 = browser.html
soup4 = soup(html2, 'html.parser')
results2 = soup4.find_all('li')[0]
# print(results2)
url2=results2.a['href']
title_url2=url+url2
# print(title_url2)


browser.visit(scrape_url_3)    
html3 = browser.html
soup5 = soup(html3, 'html.parser')
results3 = soup5.find_all('li')[0]
# print(results1)
url3=results3.a['href']
title_url3=url+url3
# print(title_url3)


browser.visit(scrape_url_4)    
html4 = browser.html
soup6 = soup(html4, 'html.parser')
results4 = soup6.find_all('li')[0]
# print(results4)
url4=results4.a['href']
title_url4=url+url4
# print(title_url4)


image_url=[title_url1, title_url2, title_url3, title_url4]


# print(image_url)
# print("***")
# print(title)


hemisphere_image_urls=[{"img_url": image_url[0],"title":title[0]},
                       {"img_url": image_url[1],"title":title[1]},
                       {"img_url": image_url[2],"title":title[2]},
                       {"img_url": image_url[3],"title":title[3]}]


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()


# # Another Way

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# loop through to get 4 different images
for i in range(4):
    
    # Create empty dictionary
    hemisphere = {}
    
    # Finding different tags to click for hemisphere
    browser.find_by_css('a.product-item h3')[i].click()
    
    # Finding sample image for hemisphere to get each sample image url
    img_url = browser.find_link_by_text('Sample')[0]['href']
    
    # Find title of hemisphere 
    title = browser.find_by_css('h2.title').text

    # Add img_url and title to dictionary and then to list
    hemisphere["img_url"] = (img_url)
    hemisphere["title"] = title    
    hemisphere_image_urls.append(hemisphere)
    
    # Return to main page
    browser.back()
    

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()
