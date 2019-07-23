"""
Raymond Atta-Fynn
New York City Data Science Academy
July 21, 2019

This script scrapes customer reviews from MGM Grand Hotel & Casino.
The Google Chrome Driver and the XPATH suite in Selenium were employed
The review parameters extracted were:
(a) title of the review
(b) Comment posted by reviewer
(c) username of the reviewer
(d) date of stay
(e) rating on a scale of 1-5.

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time

# Specify the path to chrome driver you just downloaded.
#Windows
# driver = webdriver.Chrome(r'path\to\the\chromedriver.exe')
# Ubuntu Linux
# driver = webdriver.Chrome(r'/usr/bin/chromedriver')
driver = webdriver.Chrome()
# Go to the page that we want to scrape
driver.get("https://www.tripadvisor.com/Hotel_Review-g45963-d91891-Reviews-MGM_Grand_Hotel_and_Casino-Las_Vegas_Nevada.html")

# Click review button to go to the review section
review_button = driver.find_element_by_xpath('//span[@class="reviewCount ui_link level_4"]')
review_button.click()

# Open CVS file
csv_file = open('reviews.csv', 'w', encoding='utf-8', newline='')


# Write CVS file header
writer = csv.DictWriter(csv_file,fieldnames=[" title ", " comment ", " username ", " date  ", " rating "])
writer.writeheader()

writer = csv.writer(csv_file)

# Page index used to keep track of where we are.
index = 1
# We want to start the first two pages.
# If everything works, we will change it to while True
#while index <=2:
while True:
    try:
        print("Scraping Page number " + str(index))
        index = index + 1
        # Find all the reviews. The find_elements function will return a list of selenium select elements.
        # For more information see  http://selenium-python.readthedocs.io/locating-elements.html
        reviews = driver.find_elements_by_xpath('//div[@class="hotels-review-list-parts-SingleReview__reviewContainer--d54T4"]')
        # Iterate through the list and find the details of each review.
        for review in reviews:
        # Initialize an empty dictionary for each review
            review_dict = {}
            # Use relative xpath to locate the following: title, text, username, date, rating.
            # Once you locate the element, you can use 'element.text' to return its string.
            # To get the attribute instead of the text of each element, use 'element.get_attribute()'
            # Use try and except to skip the review elements that are empty.
            try:
                title = review.find_element_by_xpath('.//div[@class="hotels-review-list-parts-ReviewTitle__reviewTitle--2Fauz"]').text
            except:
                continue

            text = review.find_element_by_xpath('.//div[@class="common-text-ReadMore__content--2X4LR"]').text
            username = review.find_element_by_xpath('.//a[@class="ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC"]').text
            date_published = review.find_element_by_xpath('.//div[@class="hotels-review-list-parts-EventDate__event_date--CRXs4"]').text
            date_published.replace('Date of stay: ','')
            rating = review.find_element_by_xpath('.//div[@class="hotels-review-list-parts-RatingLine__bubbles--1oCI4"]//span[contains(@class,text())]')
            rating = rating.get_attribute('class')
            rating = float(rating[-2:])/10

#           print('Title = {}'.format(title))
#           print('text = {}'.format(text))
#           print('username = {}'.format(username))
#           print('date_published = {}'.format(date_published.replace('Date of stay: ','')))
#           print('rating = {}'.format(rating))
            
            review_dict['title'] = title
            review_dict['text'] = text
            review_dict['username'] = username
            review_dict['date_published'] = date_published.replace('Date of stay: ','')
            review_dict['rating'] = rating
            writer.writerow(review_dict.values())

        # Locate the next button element on the page and then call `button.click()` to click it.
        button = driver.find_element_by_xpath('//a[@class="ui_button nav next primary "]')
        button.click()
        time.sleep(1)

    except Exception as e:
        print(e)
        #driver.close()
        break

#Close CVS file
csv_file.close()

#Shutdown Browser
driver.close()
