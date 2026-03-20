# Country Currency Summary API

A Django REST API project that integrates two public APIs and returns country and currency information in one unified JSON response.

## Features
- Get country details by country name
- Get currency exchange rate from USD
- Unified JSON response
- Error handling for missing or invalid input
- Swagger/OpenAPI documentation
- Simple HTML UI

## APIs Used
1. REST Countries API
2. Frankfurter API

## Main Endpoint
```bash
/api/v1/country-currency-summary/?country=Japan


Example Response
{
  "country": "Japan",
  "capital": "Tokyo",
  "region": "Asia",
  "currency_code": "JPY",
  "currency_name": "Japanese yen",
  "usd_to_currency": 149.23
}


Error Handling
400 Bad Request if the country parameter is missing
404 Not Found if the country does not exist
502 Bad Gateway if an external API request fails


Documentation
Swagger UI is available at:



/api/docs/


Simple UI
A simple HTML interface is available at:



/


How to Run
python manage.py runserver


Automated Test
Run tests using:



python manage.py test
After pasting that:

1. save `README.md`
2. run:
```bash
git add README.md
git commit -m "Add README"
git push