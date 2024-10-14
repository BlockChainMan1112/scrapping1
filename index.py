from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pymongo import MongoClient
import threading
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb+srv://jackhappy1112:hwoRy3tSgcGxD93N@cluster0.trmdr8u.mongodb.net')  # Use your MongoDB URI
db = client['scrapping']  # Use the database name
collection = db['data']

# Set up Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # Disable GPU to speed up
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable image loading

# Function to save data to the database in bulk
def save_data_to_db(scraped_data):
    collection.delete_many({})  # Clear old data
    if scraped_data:
        collection.insert_many(scraped_data)  # Bulk insert for better performance

# Function to scrape data from the table
def scrape_data(state):
    driver = webdriver.Chrome(options=chrome_options)
    
    # Dynamically generate the URL based on the state parameter
    url = f'https://racingaustralia.horse/FreeFields/Calendar_Scratchings.aspx?State={state}'
    driver.get(url)

    # Get the page source and parse it using BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the table with class 'race-fields'
    table = soup.find('table', class_='race-fields')
    
    # List to store scraped data
    scraped_data = []

    if table:
        # Find all rows in the table, skipping the header row
        rows = table.find_all('tr')[1:]

        for row in rows:
            # Extract venue date
            venue_date = row.find_all('td')[0].get_text(strip=True)

            # Extract venue name and link
            venue = row.find_all('td')[1].get_text(strip=True)
            venue_link = row.find_all('td')[1].find('a')['href']

            # Extract race time
            race_time = row.find_all('td')[2].get_text(strip=True)

            # Store the extracted data
            race_data = {
                'venue_date': venue_date,
                'venue': venue,
                'venue_link': venue_link,
                'race_time': race_time
            }
            scraped_data.append(race_data)

    # Close the driver after scraping
    driver.quit()

    return scraped_data

# Optimized function to handle scraping in parallel for multiple states (if required)
def scrape_and_save(state):
    scraped_data = scrape_data(state)
    save_data_to_db(scraped_data)  # Save the scraped data to MongoDB

# Define the Flask route for scraping with a dynamic state parameter
@app.route('/scrape/<state>', methods=['GET'])
def scrape_route(state):
    # Validate the state input
    valid_states = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']
    
    if state not in valid_states:
        return jsonify({'error': 'Invalid state code'}), 400

    # Start a new thread to scrape and save the data in the background
    threading.Thread(target=scrape_and_save, args=(state,)).start()
    
    # Perform the scraping and return data immediately
    scraped_data = scrape_data(state)
    
    # Return scraped data immediately without waiting for the database operation
    return jsonify(scraped_data), 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
