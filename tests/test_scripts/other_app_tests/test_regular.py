import sys

sys.path.append('../../')
import pytest
from business_components.get_quote import *
from PyAuto.PyAutoLogger import get_logger

logger = get_logger()


@pytest.mark.jenkinsExecute
@pytest.mark.smoke
def test_header_nav(driver):
    quote_navigate_Auto(driver)
    driver.back()
    quote_navigate_truck(driver)
    driver.back()
    quote_navigate_motor(driver)
    driver.back()
    quote_navigate_camper(driver)
    driver.back()


@pytest.mark.footer
def test_footer_nav(driver):
    footer_navigate_products(driver)
    driver.back()
    footer_navigate_events(driver)
    driver.back()
    footer_navigate_resources(driver)
    driver.back()


@pytest.mark.exception_handling
def test_autoquote_home(driver):
    autoquote_home_page_1(driver)
    enter_insurant_data_auto(driver)
    # logging.info("Logging an info message")
    # logging.debug("Logging a DEBUG message")
    # logging.warning("Sample time is too low!")

# def test_autoquote_excel_home(driver):
#     enter_data_for_quote1("TC01")


# def test_autoHome_home(driver):
#     a = AutoWebHome(driver)
#     a.navigate_insurance()
