from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import os
import time

#!which chromedriver

def scrape_data():
    executable_path = {"executable_path": "/Users/ginia/Desktop/bin/chromedriver"}
    browser= Browser("chrome", **executable_path, headless=True)
    
    news_title,news_p= scrape_mars_news(browser)
    featured_image_url= scrape_mars_images(browser)
    url = scrape_mars_twitter(browser)
    marsfacts_html = scrape_mars_facts(browser)
    hemi_list = scrape_mars_hemisphere(browser)

    mars_data={
        "mars_news_title":news_title,
        "mars_news_paragraph":news_p,
        "mars_images": featured_image_url,
        "mars_twitter" : url,
        "mars_facts" : marsfacts_html,
        "hemi_dict" : hemi_list
    }

    # Close the browser after scraping
    browser.quit()

    return mars_data
    

def scrape_mars_news(browser):

    # Visit url
    url_nasa_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_nasa_news)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Get the news
    soup1=soup.select_one("ul.item_list li.slide")
    news_title = soup1.find("div", class_ = "content_title").text
    news_p= soup1.find("div", class_ = "article_teaser_body").text

    # # Store data in a dictionary
    # mars_news = {"mars_news_title":news_title,
    #             "mars_news_paragraph":news_p}
    

    # Return results
    return news_title,news_p


def scrape_mars_images(browser):

    # Visit url
    url_mars_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_mars_image)

    # Scrape page into Soup
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)

    browser.click_link_by_partial_text('more info')
    time.sleep(5)

    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    # Get the image url
    image_url = soup2.find('figure', class_='lede')
    image_link = image_url.a["href"]
    featured_image_url='https://www.jpl.nasa.gov/' + image_link


    # Return results
    return featured_image_url


def scrape_mars_twitter(browser):

    # Visit url
    url_mars_weather='https://twitter.com/marswxreport?lang=en'
    
    # Scrape page into Soup
    response = requests.get(url_mars_weather)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #Get the twitter
    url=soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    
    # Return results
    return url



def scrape_mars_facts(browser):

    # Visit url
    url_mars_facts='https://space-facts.com/mars/'
    
    # Scrape page into Soup
    response = requests.get(url_mars_facts)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #Get the mars facts table
    mars_tables = pd.read_html(url_mars_facts)
    mars_fact_df=mars_tables[0]
    renamed_marsfacts_df = mars_fact_df.rename(columns={0:"Facts", 1:"Value"})
    # renamed_marsfacts_df1 = renamed_marsfacts_df.set_index('Facts')
        
    #Convert df to html table string
    marsfacts_html=renamed_marsfacts_df.to_html()
    

    #need to edit dataframe

    # Return results
    return marsfacts_html

def scrape_mars_hemisphere(browser):

    # Visit url
    url_mars_hemispheres='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Scrape page into Soup
    browser.visit(url_mars_hemispheres)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #Get the mars hemisphere title and images
    title=soup.find_all('div', class_="description")
    hemi_list=[]

    for x in title:
        hemi_title=x.find('a',class_="itemLink product-item").text
        hemi_image= x.a['href']
        hemisphere_image_url = url_mars_hemispheres + hemi_image
        
        hemi_dict={"title":hemi_title,"image":hemisphere_image_url}
        hemi_list.append(hemi_dict)


    # Return results
    return hemi_list

# Jeff Added Code:  ALWAYS TEST!!!
if __name__ == "__main__":
    print("\nTesting Data Retrieval...\n")
    print(scrape_data())
    print("\nProcess Complete!\n")