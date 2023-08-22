from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import time

# Set up the Selenium webdriver
driver = webdriver.Chrome()
driver.get('https://www.facebook.com')

# Log in to Facebook
email_field = driver.find_element_by_id('email')
email_field.send_keys('your_email_address')
password_field = driver.find_element_by_id('pass')
password_field.send_keys('your_password')
password_field.send_keys(Keys.RETURN)

# Wait for the page to load
time.sleep(5)

# Navigate to the Facebook group you want to scrape
group_url = 'https://www.facebook.com/groups/your_group_name'
driver.get(group_url)

# Wait for the page to load
time.sleep(5)

# Set up the CSV file
csv_file = open('facebook_posts.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Date', 'Content'])

# Scrape the posts
while True:
    # Get the HTML source code of the page
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the posts on the page
    posts = soup.find_all('div', {'class': '_5pcb _4b0l _2q8l'})

    for post in posts:
        # Get the time of the post
        time_element = post.find('abbr', {'class': '_5ptz'})
        post_time = time_element['title']

        # Check if the post contains the word 'dispo'
        post_content = post.find('div', {'class': '_5pbx userContent'})
        if 'dispo' in post_content.text:
            csv_writer.writerow([post_time, post_content.text])

    # Check if there is a 'See More' button on the page
    see_more_button = driver.find_element_by_xpath("//a[contains(@class, 'see_more_link')]")
    if see_more_button:
        see_more_button.click()
        time.sleep(5)
    else:
        break

# Close the CSV file
csv_file.close()

# Close the browser
driver.quit()
