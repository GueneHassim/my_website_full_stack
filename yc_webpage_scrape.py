### Class that manages the scraping of the Y Combinator global news session

import pandas as pd
from bs4 import BeautifulSoup
import requests

import os
import send_email

# Define the URL to scrape data from
YC_URL = "https://news.ycombinator.com/news"


class YCWebpageScraper:
    # Initialize the scraper with default sorting settings and handshake status
    def __init__(self):
        self.name_provy = "rank"  # Default sorting field
        self.reversed_provy = True  # Default sorting order
        self.handshake = False  # Status to indicate if there's a handshake

    # Function to scrape data from the Y Combinator page
    def get_data(self):
        self.response = requests.get(YC_URL)  # Perform GET request to fetch page content
        self.url_source = self.response.text  # Store the HTML response
        soup = BeautifulSoup(self.url_source, 'html.parser')  # Parse HTML content with BeautifulSoup
        self.all_posts = soup.select(".athing")  # Select all posts on the page
        date_post = soup.find_all(name="td", class_="subtext")  # Find additional post details

        self.saved_posts = []  # Initialize an empty list to store parsed posts

        # Iterate over all posts to extract relevant data
        for n_post in range(len(self.all_posts)):
            post = self.all_posts[n_post]
            rank = post.select_one('.rank').text.split(".")[0]  # Extract rank of the post
            title = post.select_one('.titleline').select_one("a").text  # Extract title
            post_url = post.select_one('.titleline').select_one("a").get('href')  # Extract URL
            if not post_url.startswith('http'):
                post_url = 'no working url'  # Handle relative URLs

            # Extract date and score information
            d = date_post[n_post]
            periodo = d.find(class_="age").get("title")  # Extract full date info
            date = d.find(class_="age").text  # Extract relative time (e.g., "3 hours ago")

            try:
                score = d.find(name='span', class_='score').text.split()[0]  # Extract score
            except AttributeError:
                score = 'no scored yet'  # Handle posts without scores

            post_punti = d.find_all('a')[-1].text.split()[0]  # Extract comments count
            commenti = post_punti if post_punti.isdigit() else 'not punti yet'  # Validate comments count

            # Append the extracted data as a dictionary to saved_posts
            self.saved_posts.append({
                "rank": rank,
                "titolo": title,
                "date info": periodo,
                "periodo": date,
                "score": score,
                "commenti": commenti,
                "url": post_url
            })

        return self.saved_posts  # Return the list of parsed posts

    # Read content from 'dati.csv' as a string
    def read(self):
        with open('dati.csv', 'r') as file:
            return file.read()

    # Read CSV data into a pandas DataFrame
    def reading(self):
        df = pd.read_csv('data.csv')
        return df

    # Function to read sorted DataFrame and output it as a list of dictionaries for web page population
    def leggi_sort(self):
        df = self.reading()  # Read the CSV into a Data
