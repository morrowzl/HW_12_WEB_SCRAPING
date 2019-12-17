from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # LATEST NEWS
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    latest_news_title = soup.find("div", class_="content_title").text.strip()
    news_tease = soup.find("div", class_="article_teaser_body").text.strip()
    article_link = news_url + soup.find("div", class_="content_title").a['href']
    
    # FEATURED IMAGE
    featured_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    image_path = soup.find_all("div", class_="grid_layout")[2].find_all("div", class_="img")[0].img['src']
    image_id = (image_path.split("/")[4]).split("-")[0]
    high_res_url = f"https://www.jpl.nasa.gov/spaceimages/images/largesize/{image_id}_hires.jpg"

    # WEATHER
    twit_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twit_url)
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    mars_weather = (soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()).split("pic")[0]

    # FACT TABLE
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(1)

    fact_table_df = pd.DataFrame(pd.read_html(facts_url)[0])
    fact_table_df.to_html('table.html', header=False, index=False)

    # HEMISPHERES
    hemisphere_list = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
    ]

    # Store data in a dictionary
    mars_data = {
        "latest_news_title": latest_news_title,
        "news_tease": news_tease,
        "article_link": article_link,
        "high_res_url": high_res_url,
        "mars_weather": mars_weather,
        "valles_title": hemisphere_list[0]['title'],
        "valles_img_url": hemisphere_list[0]['img_url'],
        "cerberus_title": hemisphere_list[1]['title'],
        "cerberus_img_url": hemisphere_list[1]['img_url'],
        "schia_title": hemisphere_list[2]['title'],
        "schia_img_url": hemisphere_list[2]['img_url'],
        "syrt_title": hemisphere_list[3]['title'],
        "syrt_img_url": hemisphere_list[3]['img_url']
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
