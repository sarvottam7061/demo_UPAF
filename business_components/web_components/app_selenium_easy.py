from object_repository.pages.AppInputForm import InputForm
from object_repository.pages.BootstrapListBox import ListBox

from PyAuto.PyAutoLogger import get_logger

import allure

logger = get_logger()


# Use method chaining by creating an object from the page name
@allure.step("submit user information step 2")
def input_form_test_data_step_2(driver, state, zip_code, website, hosting, project_desc):
    InputForm(driver).select_state(state).enter_zip(zip_code).enter_web(website) \
        .radio_hosting(hosting).enter_desc(project_desc).take_screenshot().click_send()


@allure.step("submit user information step 1")
def input_form_test_data_step_1(driver, fname, lname, email, phone, Address,
                                city):
    InputForm(driver).navigate().enter_fname(fname).enter_lname(lname).enter_email(email).enter_phone(phone) \
        .enter_address(Address).enter_city(city)

@allure.step("check visibility of search box")
def is_search_box_visible(driver):
    ListBox(driver).navigate().is_visible()


