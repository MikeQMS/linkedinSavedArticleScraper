# LinkedIn Saved Article Scrapper
* This little tool will scrape your stored / saved articles from LinkedIn.com, then save the details to a
    database and display them in a simple form


## How to use
* install all required files from pipfile+
* enter your login information in the credentials.ini
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


### Version 0.1

### TODO:
* testing the system with more than 4 articles saved
* adding this application to docker container
* take username and password as argument on startup
* store username and password encrypted in database file

Please let me know when you have further suggestions, requests or bugs. 
