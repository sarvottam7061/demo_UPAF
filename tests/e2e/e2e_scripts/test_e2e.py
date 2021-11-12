import pytest

from business_components.database_components.payment_table_component import *
from business_components.web_components.app_selenium_easy import *
from business_components.api_components.reqres_components import *
from business_components.database_components.actor_table_components import *
from business_components.mobile_components.app_flipkart import *
from business_components.mobile_components.app_ecommerce import *



# you can call the test function directly as a test step in e2e tests
from utilities.helper import read_json_for_soap


@pytest.mark.e2e
def test_e2e(driver, rest_client, db_connection):
    names = get_user_name_load(driver)
    write_to_excel(names)
    validate_post_user_creation(rest_client)
    check_record_exists_full_name(db_connection)



















@pytest.mark.e2e_soap
def test_e2eeee(driver, soap_client, db_connection):
    download_progress(driver)
    values = fetch_dynamic_data(driver)
    assert values is not None
    write_values_excel(values)
    request_values = read_json_for_soap("listOfCountries.json")
    response = soap_client.service.CapitalCity(request_values['India'])
    assert response == "New Delhi"
    sum_of_all_payments(db_connection)
    num_of_payment_greater_8(db_connection)
    payment_average(db_connection)
    validate_payment_between(db_connection)


@pytest.mark.e2e_rest
def test_e2e_post(driver, rest_client, db_connection):
    download_progress(driver)
    values = fetch_dynamic_data(driver)
    assert values is not None
    write_values_excel(values)
    name = read_excel_first_name()
    json_data = {"name": name, "job": "leader"}
    validate_user_creation(rest_client, json_data)
    
    
@pytest.mark.e2e_rest_db
def test_e2e_post_query(driver, rest_client, db_connection):
    names = get_user_name_load(driver)
    write_to_excel(names)
    validate_post_user_creation(rest_client)
    check_record_does_not_exists_first_name(db_connection)


@pytest.mark.e2e_mobile
def test_e2e_mobile(mobile_conn):
    # input_form_test_data_step_1(driver, "fname", "lname", "email@emaol.com", "12345", "Address", "city")
    # # validate_post_user_creation(rest_client)
    search_iphone(mobile_conn)
    # checkout_form_fillup(mobile_conn, "Prateek Das", "A Sample Comment")


    






