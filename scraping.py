#!/usr/bin/env python
# coding: utf-8


# Import Splinter and BeautifulSoup  and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
#import pyppdf.patch_pyppeteer



def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return "ok", "ok"

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return "ok"

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return "ok"

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())








# def scrape_all():
#     # Initiate headless driver for deployment
#     executable_path = {'executable_path': ChromeDriverManager().install()}
#     browser = Browser('chrome', **executable_path, headless=True)
# # #setup splinter
# # executable_path = {'executable_path': ChromeDriverManager().install()}
# # browser = Browser('chrome', **executable_path, headless=False)
# #headless = False - can see the scrap in action
# #headless = True - don't see the scrape in action

#     news_title, news_paragraph = mars_news(browser)

# # Run all scraping functions and store results in dictionary
#     data = {
#         "news_title": news_title,
#         "news_paragraph": news_paragraph,
#         "featured_image": featured_image(browser),
#         "facts": mars_facts(),
#         "last_modified": dt.datetime.now()
# }

#     # Stop webdriver and return data
#     browser.quit()
#     return data

# def mars_news(browser):
#     # Visit the mars nasa news site
#     url = 'https://redplanetscience.com'
#     browser.visit(url)
#     # Optional delay for loading the page
#     browser.is_element_present_by_css('div.list_text', wait_time=1)
#     #setup HTML parser
#     html = browser.html
#     news_soup = soup(html, 'html.parser')
#     # add try/except for error handling
#     try:
#         #parent element - holds all elements within it and we'll reference when we want to filter results further
#         slide_elem = news_soup.select_one('div.list_text')
#         #article title assignment
#         slide_elem.find('div',class_="content_title")

#         #use parent element to find the first "a" tag and savie it as "news_title"
#         news_title=slide_elem.find('div',class_="content_title").get_text()
        
#         #article summary assignment
#         slide_elem.find('div',class_="artcile_teaser_body")

#         news_p=slide_elem.find('div',class_="article_teaser_body").get_text()
#     except AttributeError:
#         return None, None
#     return news_title, news_p

# # ### Featured Images

# def featured_image(browser):
#     # Visit URL
#     url = 'https://spaceimages-mars.com'
#     browser.visit(url)
#     # Find and click the full image button
#     full_image_elem = browser.find_by_tag('button')[1]
#     full_image_elem.click()
#     #setup HTML parser
#     html = browser.html
#     img_soup = soup(html, 'html.parser')
#     #find the relative image url
#     #look inside image tag for an image with class fancybox_image
#     #doing it this way will allow you to grab the most recent one
#     try:
#         # find the relative image url
#         img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
#     except AttributeError:
#         return None

#     #use base url to create an absoulte url
#     img_url=f'{url2}{img_url_rel}'
#     return img_url

# #Instead of scraping each row, or the data in each <td />, 
# #we're going to scrape the entire table with Pandas' .read_html() function.
# #read_html will specifically search for a table and the [0] has it only searching for the first table it sees
# #there are two on this site, then it will turn it into a data frame
# def mars_facts():
#     try:       
#         df=pd.read_html('https://galaxyfacts-mars.com')[0]
#     except BaseException:
#         return None
#     df.columns=['Description',"Mars","Earth"]
#     #changing description column into dataframe index
#     df.set_index('Description', inplace=True)
#     return df.to_html()

# #This last block of code tells Flask that our script is complete and ready for action
# if __name__ == "__main__":
#     # If running as script, print scraped data
#     print(scrape_all())


