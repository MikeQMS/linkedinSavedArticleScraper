import os

import django
# django.setup()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import configparser


def run(isSecurityChallange):
    # set options for chromium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("disable-popup-blocking")

    # run it as background job, but only works when no captcha check
    if not isSecurityChallange:
        options.add_argument("headless")

    # parse configfile with username and password
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.abspath(__file__)) + './credentials.ini')
    username = config['Login']['username']
    password = config['Login']['password']
    # create Chrome webdriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # get to linkedin login page
    driver.get("https://www.linkedin.com/login/")

    # pass username and password to form and click button
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        # decline cookies
        if button.text == "Ablehnen":
            button.click()
        # Login Button
        if button.text == "Einloggen":
            button.click()
            break
    if driver.current_url.startswith("https://www.linkedin.com/checkpoint/challenge") == True and isSecurityChallange == False:
        run(True)
    # When there is a challenge while login, the programm will remain until captcha is manually solved
    while driver.current_url.startswith("https://www.linkedin.com/checkpoint/challenge"):
        continue

    # page with the posts to be scraped
    driver.get("https://www.linkedin.com/my-items/saved-posts/")
    articles = driver.find_elements(By.CLASS_NAME, "entity-result")
    articleCollector = []
    for article in articles:
        #get the profile image URL
        container = article.find_element(By.CLASS_NAME, "entity-result__content-image")
        image = container.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

        #Get name of whom shared the article
        actor = article.find_element(By.XPATH, ".//span[@dir]/span[@aria-hidden]")

        #get the Subtitle / Article desciption
        contentActor = article.find_element(By.CLASS_NAME, "entity-result__content-actor")
        subtitle = contentActor.find_element(By.CLASS_NAME, "entity-result__primary-subtitle")

        #get the name of who shared the article
        shared = contentActor.find_element(By.CSS_SELECTOR, "p")

        #get the content image URL
        content = article.find_element(By.CLASS_NAME, "entity-result__content-inner-container")
        contentImage = content.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

        #get the content summary
        contentContainer = content.find_element(By.CLASS_NAME, "entity-result__content-summary")
        contentSummary = contentContainer.find_element(By.CSS_SELECTOR, "span")

        #get the content link
        contentLink = content.find_element(By.CLASS_NAME, "app-aware-link").get_attribute("href")


        # For local testing purpose only
        if __name__ == "__main__":
            class SavedPost:
                def __init__(self, image="", title="", subtitle="", sharedby="", contentImage="", contentLink="",
                             contentSummary=""):
                    self.image = image
                    self.title = title
                    self.subtitle = subtitle
                    self.sharedby = sharedby
                    self.contentImage = contentImage
                    self.contentLink = contentLink
                    self.contentSummary = contentSummary
            articleCollector.append(
            SavedPost(image, actor.text, subtitle.text, shared.text, contentImage, contentSummary.text, contentLink))
            print(articleCollector.__str__())
        else:
            # creates a django model
            post = Posts(image=image, title=actor.text, subtitle=subtitle.text, shared_by=shared.text, content_image=contentImage,
                     content_link=contentLink, content_summary=contentSummary.text)
            # checks if article link already in database
            if not Posts.objects.all().filter(content_link=contentLink):
                # saves post to database if not exists
                post.save()
    driver.close()


if __name__ == "__main__":
    run(False)
else:
    from .models import Posts
