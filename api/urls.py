from django.urls import path
from .views import CountryCurrencySummaryView

urlpatterns = [
    path("v1/country-currency-summary/", CountryCurrencySummaryView.as_view(), name="country-currency-summary"),
]

#Write automated tests for API validation and error respo