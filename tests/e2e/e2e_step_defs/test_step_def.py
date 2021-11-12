from business_components.web_components.app_selenium_easy import *
import logging
from business_components.api_components.reqres_components import *
from pytest_bdd import scenarios, given, when, then

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

scenarios('../e2e_features/e2e.feature')


@given("I check the download progress")
def check_download_progress(bdd_driver):
    download_progress(bdd_driver)


@when("I fetch the name and write it in excel file")
def fetch_and_write_data(bdd_driver):
    values = fetch_dynamic_data(bdd_driver)
    assert values is not None
    write_values_excel(values)


@then("I create an user using first name")
def create_user_using_name(rest_client):
    name = read_excel_first_name()
    json_data = {"name": name, "job": "leader"}
    validate_user_creation(rest_client, json_data)


@when("I read the data written and validate it")
def read_and_validate_data():
    pass
