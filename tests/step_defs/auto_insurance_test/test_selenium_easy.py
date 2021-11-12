from pytest_bdd import scenarios, given, when, then, parsers
import sys

sys.path.append('../../')
import pytest
from selenium import webdriver
from object_repository.pages.AppInputForm import InputForm


scenarios('../../features/selenium_easy.feature')


@given("I am on selenium easy page and i navigate to input forms page")
def navigate_to_inputforms(bdd_driver):
    InputForm(bdd_driver).navigate()


@when("I enter valid <first_name> in First Name field")
def enter_first_name(bdd_driver, first_name):
    InputForm(bdd_driver).enter_fname(first_name)


@when("I enter valid <last_name> in Last Name field")
def enter_last_name(bdd_driver, last_name):
    InputForm(bdd_driver).enter_lname(last_name)


@when("I enter valid <email> in Email field")
def enter_email_id(bdd_driver, email):
    InputForm(bdd_driver).enter_email(email)


@when("I enter valid <phone> in phone number field")
def enter_phone_num(bdd_driver, phone):
    InputForm(bdd_driver).enter_phone(phone)


@when("I enter valid <address> in Address field")
def enter_address(bdd_driver, address):
    InputForm(bdd_driver).enter_address(address)


@when("I enter valid <city> in city field")
def enter_city(bdd_driver, city):
    InputForm(bdd_driver).enter_city(city)


@when("I select valid <state> in state dropdown")
def enter_state(bdd_driver, state):
    InputForm(bdd_driver).select_state(state)


@when("I enter valid <zip_code> in zip code field")
def enter_zip_code(bdd_driver, zip_code):
    InputForm(bdd_driver).enter_zip(zip_code)


@when("I choose <yes_or_no> in for Do you have a hosting")
def enter_yes_or_no(bdd_driver, yes_or_no):
    InputForm(bdd_driver).radio_hosting(yes_or_no)


@when("I enter valid <project_description> in description field")
def enter_project_description(bdd_driver, project_description):
    InputForm(bdd_driver).enter_desc(project_description)


@when(parsers.parse('I enter valid website or domain name as "{url}"'))
def enter_website_or_domain(bdd_driver, url):
    InputForm(bdd_driver).enter_web(url)


@then("I submit the form")
def submit_form(bdd_driver):
    InputForm(bdd_driver).click_send()
