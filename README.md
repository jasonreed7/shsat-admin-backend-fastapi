# SHSAT Admin Backend
This is a Python and FastAPI service for admin management of the SHSAT app.

## Prerequisites
Follow software setup document pinned in #shsat-project Slack channel.

## Clone the repo
```
git clone https://github.com/jasonreed7/shsat-admin-backend-fastapi.git

cd shsat-admin-backend-fastapi
```

## Install dependencies
`pipenv install`

## Create the database
Only needs to be done once. In pgadmin, create a database called `shsat` and then copy and run everything from `db_schema/schema.sql` on the new database.

## Running the API
Get .env file from the team for environment variable configuration. Make sure the selected Python interpreter in VS Code is from your virtual environment. 

In VS Code, in the sidebar hit the play button/ bug icon. At the top left a green play button should appear. Click that.

To check that the app is running, go to `localhost:8000` in a browser and a message should appear.