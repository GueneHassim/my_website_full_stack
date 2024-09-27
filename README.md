# GueneTh - Full Stack Web Application

This project is a Flask-based full-stack web application developed as a personal website. It features multiple sections including a blog, portfolio, and contact form. The site is designed to showcase various personal projects, such as a Y Combinator scraper, and aims to continuously grow with new projects and enhancements over time.

The site is live and accessible at www.gueneth.com.

Features
Home Page
A welcoming section introducing the site's content and the developer.

Portfolio
A dedicated space to showcase completed and ongoing projects. Projects like the Y Combinator scraper are described in detail, with the potential for new projects to be added as they are developed.

Blog
A blogging platform where insights, experiences, or updates on development projects are shared.

Scrape Y Combinator News
A section dedicated to scraping and displaying the latest news data from Y Combinator. Extracted details include the rank, title, date, score, and comments. The scraped data is saved in a CSV file and displayed dynamically on the web page.

Contact Form
A contact section where users can reach out via a form. Upon submission, the information is stored in a MongoDB database and also sent via email to the site owner for prompt communication.

Download CV
Users have the option to download the developer's CV after filling out the contact form.

Continuous Upgrades
The website is a work in progress, with regular updates to both the site’s design and functionality, as well as the addition of new projects to the portfolio.

Project Structure
app.py:
The main Flask application that handles routing for different sections (blog, portfolio, scraper, contact form).

yc_webpage_scrape.py:
Contains the YCWebpageScraper class, responsible for scraping and processing the latest news data from the Y Combinator website.

send_email.py:
Handles sending emails containing contact form details using SMTP to a specified recipient.

write_contact_db.py:
Includes the WriteContactDb class for storing contact form submissions in a MongoDB database for easy record-keeping and data management.

Setup & Usage
Clone the Repository

bash
Copy code
git clone <repository-url>
cd <project-directory>
Install Dependencies
Ensure you have Flask, BeautifulSoup, pandas, pymongo, and other required packages.

bash
Copy code
pip install -r requirements.txt
Configure Environment Variables
Set up your MongoDB Atlas connection string, SMTP email details, and other environment variables as needed.

Run the Application

Notes

Security: Ensure to replace placeholders like YOUR_EMAIL, YOUR DB, and YOUR DB COLLECTION with your actual data.
SMTP Configuration: The email sending functionality requires configuring an SMTP server, currently set to Gmail in send_email.py.
Technologies Used
Flask for the web framework
BeautifulSoup for web scraping
pandas for data handling
MongoDB for storing contact form submissions
SMTP for sending contact form data via email

Technologies Used
Flask for the web framework
BeautifulSoup for web scraping
pandas for data manipulation
MongoDB for storing contact form submissions
SMTP for sending contact details via email
Future Improvements
Project Expansion: Continuously adding new project descriptions and examples to the portfolio section.
Site Upgrades: Regular updates and improvements to both functionality and design.
New Sections & Features: Additional sections or interactive elements to enhance user experience and showcase skills.
