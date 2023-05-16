# SHSAT Admin Backend
This is a Python and FastAPI service for admin management of the SHSAT app.

## Clone the repo
```
git clone https://github.com/jasonreed7/shsat-admin-backend-fastapi.git
cd shsat-admin-backend-fastapi
```

## Create virtual environment
You only need to do this once. Open a command line in the root directory of the project and run:
```
python -m venv venv
```

## Activate virtual environment
On Mac: `source venv/bin/activate`

On Windows: `venv\Scripts\activate`

## Install dependencies
Install pipenv if not installed already: `pip install pipenv`

Install dependencies: `pipenv sync`

## Create the database
Only needs to be done once. In pgadmin, create a database called shsat and then copy and run everything from `db_schema/schema.sql` on the new database.

## Running the API
In VS Code, in the sidebar hit the play button/ bug icon. At the top left a green play button should appear. Click that.

To check that the app is running, go to `localhost:8000` in a browser and a message should appear.