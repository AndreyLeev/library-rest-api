# library-rest-api
REST API for the Library App.

## Start project in local
* docker-compose build
* docker-compose up

## API Endpoints

* **/api/user/** (User create and list endpoint)
* **/api/users/{user-username}/** (User retrieve, update and destroy endpoint)
* **/api/users/{user-username}/book/** (Book create and list endpoint for certain user)
* **/api/users/{user-username}/book/{book-id}/** (Book retrieve, update and destroy endpoint)
