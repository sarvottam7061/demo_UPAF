import allure
import pytest
from config import TestConfig as config
from PyAuto.PyAutoReadWrite import ReadWrite
from utilities.helper import convert_to_json, read_json_for_soap

from PyAuto.PyAutoLogger import get_logger

logger = get_logger()


@pytest.mark.soap_tests
@allure.step("retrieve country code and validate capital")
def test_retrieve_country_code_validate_capital(soap_client):
    request_values = read_json_for_soap("listOfCountries.json")
    response = soap_client.service.CapitalCity(request_values['India'])
    assert response == "New Delhi"



