# LinkedIn Saved Article Scrapper
* This little tool will scrape your stored / saved articles from LinkedIn.com, then save the details to a
    database and display them in a simple form


## How to use

### Docker

* Just pull and run the docker container

    
    docker pull mikeqms/linkedinsavedarticlescraper:latest
    docker run -p 8000:8000 mikeqms/linkedinsavedarticlescraper

* to access the application enter in your browser (when the container runs in docker)


    http://127.0.0.1:8000


### Within IDE (i used Pycharm)
* install all required files from pipfile / requirements.txt
* run django in terminal
    

    python .\manage.py runserver


* go to page

    
    http://127.0.0.1:8000/

* if after the page is loaded, it is empty, you might just refresh the page
* to call the API use


    http://127.0.0.1:8000/api




### Delete and recreate a empty Database file
* just remove the db.sqlite3 file
* then run in terminal


    python .\manage.py migrate


## Version 0.1.3
* dockerized the application

## Version 0.1.2
* login details can be entered on main page

## Version 0.1.1
* added a search function to the main page

### Version 0.1

### TODO:
* testing the system with more than 4 articles saved
* still some issues inside the docker container especially when it comes to the linkedin challenge


Please let me know when you have further suggestions, requests or bugs. 
