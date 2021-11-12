import sys

sys.path.append('../../')
import pytest
from config import TestConfig as config
from business_components.web_components.get_quote import *
from PyAuto.PyAutoLogger import get_logger
logger = get_logger()
from utilities.helper import *


@pytest.mark.excel_data_driven
@pytest.mark.parametrize("fname, lname, email, phone, Address, city, state, zip_code, website, hosting, project_desc",
                         parametrized_test_data_excel_fetch("TestData.xlsx", "TC-01"))
def test_send_input_form(driver, fname, lname, email, phone, Address, city, state, zip_code, website, hosting,
                         project_desc):
    input_form_test_data(driver, fname, lname, email, phone, Address, city, state, zip_code, website, hosting,
                         project_desc)


@pytest.mark.json_data_driven
@pytest.mark.parametrize("make, ep, dom, noOFSeats, fuel_type, lp,license_plate,  mileage",
                         parametrized_test_data_excel_fetch("TestData.xlsx", "General"))
def test_autoquote_home(driver, make, ep, dom, noOFSeats, fuel_type, lp, license_plate, mileage):
    autoquote_home_page_test_data(driver, make, ep, dom, noOFSeats, fuel_type, lp, license_plate, mileage)


@pytest.mark.parametrize("make, ep, dom, noOFSeats, fuel_type, lp,license_plate,  mileage",
                         parametrized_test_data_json_fetch("TestData.json", "TC-01"))
@pytest.mark.smoke
def test_autoquote_home(driver, make, ep, dom, noOFSeats, fuel_type, lp, license_plate, mileage):
    autoquote_home_page_test_data(driver, make, ep, dom, noOFSeats, fuel_type, lp, license_plate, mileage)

# def test_write_func_excel():
#     global excel_test_data_TC_01
#     global tc01etd
#     include_index = False
#     excel_test_data_TC_01.write_excel(tc01etd, "D:\\PyAutomation\\testData\\", "Test_Data_Modified.xlsx", "TC-03", include_index)
#
# def test_write_func_json():
#     global json_test_data
#     global jtd
#     json_test_data.write_json(jtd, "D:\\PyAutomation\\testData\\", "Test_Data_Modified.json", )
