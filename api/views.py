import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def home(request):
    return render(request, 'index.html')


class CountryCurrencySummaryView(APIView):
    def get(self, request):
        country_name = request.query_params.get("country")
        
        #error handling 400,404,500,502
        if not country_name:
            return Response(
                {"error": "Query parameter 'country' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Call The Country API
            country_url = f"https://restcountries.com/v3.1/name/{country_name}" 
            country_response = requests.get(country_url, timeout=10)

            if country_response.status_code != 200:
                return Response(
                    {"error": "Country not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            country_data = country_response.json()

            if not country_data or not isinstance(country_data, list):
                return Response(
                    {"error": "No country data found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            country = country_data[0]

            name = country.get("name", {}).get("common", "Unknown")
            capital_list = country.get("capital", [])
            capital = capital_list[0] if capital_list else "N/A"
            region = country.get("region", "N/A")

            currencies = country.get("currencies", {})
            if not currencies:
                return Response(
                    {"error": "Currency data not available for this country."},
                    status=status.HTTP_404_NOT_FOUND
                )

            currency_code = list(currencies.keys())[0]
            currency_info = currencies[currency_code]
            currency_name = currency_info.get("name", "Unknown currency")

            # If currency is USD, exchange rate is 1
            if currency_code == "USD":
                exchange_rate = 1.0
            else:
                # Call Currency API
                currency_url = f"https://api.frankfurter.app/latest?from=USD&to={currency_code}"
                currency_response = requests.get(currency_url, timeout=10)

                if currency_response.status_code != 200:
                    return Response(
                        {"error": "Failed to retrieve exchange rate data."},
                        status=status.HTTP_502_BAD_GATEWAY
                    )

                currency_data = currency_response.json()
                rates = currency_data.get("rates", {})

                if currency_code not in rates:
                    return Response(
                        {"error": "Exchange rate data missing for this currency."},
                        status=status.HTTP_404_NOT_FOUND
                    )

                exchange_rate = rates[currency_code]

            result = {
                "country": name,
                "capital": capital,
                "region": region,
                "currency_code": currency_code,
                "currency_name": currency_name,
                "usd_to_currency": exchange_rate
            }

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException:
            return Response(
                {"error": "External API request failed."},
                status=status.HTTP_502_BAD_GATEWAY
            )
        except Exception:
            return Response(
                {"error": "Something went wrong on the server."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )