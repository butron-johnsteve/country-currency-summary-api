from django.test import TestCase
from rest_framework.test import APIClient


class CountryCurrencySummaryTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_missing_country_parameter_returns_400(self):
        response = self.client.get('/api/v1/country-currency-summary/')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "Query parameter 'country' is required."}
        )