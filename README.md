# library-rest-api
REST API for the Library App.

## API Endpoints

* **/api/user/** (User create and list endpoint)
* **/api/users/{user-username}/** (User retrieve, update and destroy endpoint)
* **/api/users/{user-username}/book/** (Book create and list endpoint for certain user)
* **/api/users/{user-username}/book/{book-id}/** (Book retrieve, update and destroy endpoint)

## Start project in local
* docker-compose build
* docker-compose up

## Run tests for Library app
* docker-compose run web python src/manage.py test library 
