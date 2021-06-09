import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ### NASA Mars News
    # Visit redplanetscience.com
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the news title
    news_title = soup.find_all('div', class_='content_title')[0].text

    # Get the paragraph text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    
    ### JPL Mars Space Images - Featured Image
    # Visit spaceimages-mars.com
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find the url for the featured image
    featured_image = soup.find_all('img')[1]["src"]
    featured_image_url = url + featured_image

    ### Mars Facts
    # Set url to scrape
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # Read url's html
    tables = pd.read_html(url)

    # Select required table and set into a dataframe using indexing
    mars_df = tables[0]

    # Set column names
    mars_df.columns = ['Description', 'Mars', 'Earth']

    # Drop top row
    mars_df = mars_df.drop([0])

    # Set index
    mars_df = mars_df.set_index('Description')

    # Convert dataframe data to html data string
    mars_table = mars_df.to_html(classes=["table-hover", "table-striped"])

    # Clean up html data string by removing unwanted new lines (\n)
    mars_table = mars_table.replace('\n', '')

    # Save the datafram directly to a file in html format
    mars_df.to_html('table.html')


    ### Mars Hemispheres
    # Visit spaceimages-mars.com
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find hemisphere items to extract from html
    mars_hemisphere = soup.find('div', class_ = 'collapsible results')
    mars_items = mars_hemisphere.find_all('div', class_ = 'item')
    
    # Set empty list to store hemisphere title and image URLs
    hemisphere_image_urls = []

    # Loop through hemisphere items to extract hemisphere title and to visit each link to obtain full image url, storing both in a dictionary and then appending each dictionary to the empty list
    for item in mars_items:

        # Extract hemisphere title
        hemisphere = item.find('div', class_ = 'description')
        title = hemisphere.h3.text

        # Extract image url
        hemisphere_url = hemisphere.a["href"]
        browser.visit(url + hemisphere_url)
        html = browser.html
        soup = bs(html, "html.parser")
        img_url_path = soup.find('li').a["href"]
        img_url = url + img_url_path

        # Store the hemisphere title and image url into a dictionary
        dict = {
            "title" : title,
            "img_url" : img_url
        }

        # Append the dictionary into the previously created list
        hemisphere_image_urls.append(dict)
        

    # Store all scraped data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_table": mars_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data