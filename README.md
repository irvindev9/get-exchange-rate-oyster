# Oyster Technical Test

Exchange Api from:

- Diario Oficial de la Federación - No API provided, so you will need to scrape the site
- Fixer - Well documented API in JSON format
- Banxico - Service SF43718. API returns XML.

## Endpoints

[/api/](/api/) returns the exchange api from the three sources

[/api/token/](/api/token/) get a token to use the api

[/api/token/refresh/](/api/refresh/) refresh the token if expired


## Authentication

I use JWT for authentication.

Use the header:

> `Authorization: Bearer <token>`

Get the token from [/api/token/](/api/token/) 

You can use the following user to test the API:

> `username: oyster`

> `password: oyster123`

## Techinal Details

- Python 3.x
- Django
- Sqlite3
- JWT
- Requests

