# import os
import configparser
import os

# import django
# django.setup()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# import configparser
import platform


def run(is_security_challange, request=0):
    # set options for chromium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("disable-popup-blocking")

    # if no security challenge, start headless browser
    if not is_security_challange:
        options.add_argument("headless")

    # Options for Docker Container under Linux
    if platform.system() == "Linux":
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # create Chrome webdriver in Docker under linux
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options, executable_path='/usr/bin/chromedriver')
    else:
        # create Chrome webdriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    if request==0:
        #parse configfile with username and password
        config = configparser.RawConfigParser()
        path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        config.read(os.path.join(path, 'credentials.ini'))
        username = config['Login']['username']
        password = config['Login']['password']
    else:
        # gets username and password from the form via request.POST
        username = request["your_name"]
        password = request["your_password"]
    # get to linkedin login page
    driver.get("https://www.linkedin.com/login/de")
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
    if driver.current_url.startswith(
            "https://www.linkedin.com/checkpoint/challenge") == True and is_security_challange == False:
        run(True)
    # When there is a challenge while login, the programm will remain until captcha is manually solved
    while driver.current_url.startswith("https://www.linkedin.com/checkpoint/challenge"):
        continue
    # page with the posts to be scraped
    driver.get("https://www.linkedin.com/my-items/saved-posts/")
    articles = driver.find_elements(By.CLASS_NAME, "entity-result")
    articleCollector = []
    for article in articles:
        # get the profile image URL
        container = article.find_element(By.CLASS_NAME, "entity-result__content-image")
        image = container.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

        # Get name of whom shared the article
        actor = article.find_element(By.XPATH, ".//span[@dir]/span[@aria-hidden]")

        # get the Subtitle / Article desciption
        contentActor = article.find_element(By.CLASS_NAME, "entity-result__content-actor")
        subtitle = contentActor.find_element(By.CLASS_NAME, "entity-result__primary-subtitle")

        # get the name of who shared the article
        shared = contentActor.find_element(By.CSS_SELECTOR, "p")

        # get the content image URL
        content = article.find_element(By.CLASS_NAME, "entity-result__content-inner-container")
        contentImage = content.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

        # get the content summary
        contentContainer = content.find_element(By.CLASS_NAME, "entity-result__content-summary")
        contentSummary = contentContainer.text

        # get the content link
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
                SavedPost(image, actor.text, subtitle.text, shared.text, contentImage, contentSummary,
                          contentLink))
        else:
            # creates a django model
            post = Posts(image=image, title=actor.text, subtitle=subtitle.text, shared_by=shared.text,
                         content_image=contentImage, content_link=contentLink, content_summary=contentSummary)
            # checks if article link already in database
            if not Posts.objects.all().filter(content_link=contentLink):
                # saves post to database if not exists
                post.save()
    driver.close()


if __name__ == "__main__":
    run(True, request=0)
else:
    from .models import Posts
