import sys
import pytest
from config import TestConfig as config

sys.path.append("../../../")
from business_components.web_components.app_selenium_easy import *
import logging

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
from utilities.helper import *
from PyAuto.PyAutoReadWrite import ReadWrite


@pytest.mark.se_input_form
def test_single_send_input_form(driver):
    input_form_test_data_step_1(driver, "test", "test1", "tester03@gmail.com",
                                "7448529709", "Cognizant Test", "Newyork")
    input_form_test_data_step_2(driver, "Washington", "98076", "cognizant.com", "yes", "pytest framework")


@pytest.mark.excel_data_driven_se
@pytest.mark.parametrize("fname, lname, email, phone, Address, city, state, zip_code, website, hosting, project_desc",
                         parametrized_test_data_excel_fetch(config.testDataFileName, "TC-01"))
def test_multiple_send_input_form(driver, fname, lname, email, phone, Address, city, state, zip_code, website,
                                  hosting, project_desc):
    input_form_test_data_step_1(driver, fname, lname, email, phone, Address, city)
    input_form_test_data_step_2(driver, state, zip_code, website, hosting, project_desc)





@pytest.mark.check_search_box_visible
def test_search_box_is_visible(driver):
    is_search_box_visible(driver)

