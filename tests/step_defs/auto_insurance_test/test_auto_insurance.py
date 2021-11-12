from pytest_bdd import scenarios, given, when, then, parsers
import sys
sys.path.append('../../')
import pytest
from selenium import webdriver
from business_components.web_components.get_quote import *
from business_components.web_components.auto_quote import *

scenarios('../../features/insurance_navigate.feature')
scenarios('../../features/auto_quote.feature')


@given("I am on autoQuoteHomePage")
def auto_quote(bdd_driver):
    assert bdd_driver.current_url == "http://sampleapp.tricentis.com/101/", "The url did not match"


@then("I Validate the header links")
def header_link_validate(bdd_driver):
    quote_navigate_Auto(bdd_driver)
    bdd_driver.back()
    quote_navigate_truck(bdd_driver)
    bdd_driver.back()
    quote_navigate_motor(bdd_driver)
    bdd_driver.back()
    quote_navigate_camper(bdd_driver)
    bdd_driver.back()


@then("I Validate the footer links")
def footer_link_validate(bdd_driver):
    footer_navigate_products(bdd_driver)
    bdd_driver.back()
    footer_navigate_events(bdd_driver)
    bdd_driver.back()
    footer_navigate_resources(bdd_driver)
    bdd_driver.back()


@when("I navigate to enter details automobile quote page")
def navigate_automobile_quote(bdd_driver):
    quote_navigate_Auto(bdd_driver)


@when("I select the make value as <make>")
def select_make(bdd_driver, make):
    autoquote_select_make(bdd_driver, make)


@when("I enter <ePerformance> value in Engine Performance text box")
def enter_ePerform(bdd_driver, ePerformance):
    autoquote_enter_ePerform(bdd_driver, ePerformance)


@when("I enter <dom> value in Date of manufacture date picker")
def enter_dom(bdd_driver, dom):
    autoquote_enter_dom(bdd_driver, dom)


@when("I select the number of seats as <nos>")
def select_nos(bdd_driver, nos):
    autoquote_select_nos(bdd_driver, nos)


@when("I select the fuel type as <fuelType>")
def select_fuel_type(bdd_driver, fuelType):
    autoquote_select_FT(bdd_driver, fuelType)


@when("I enter <listPrice> value in list price text box")
def enter_list_price(bdd_driver, listPrice):
    autoquote_enter_list_price(bdd_driver, listPrice)


@when("I enter <listPrice> value in list price text box")
def enter_list_price(bdd_driver, listPrice):
    autoquote_enter_list_price(bdd_driver, listPrice)


@when("I enter <licensePlateNum> value in license plate number text box")
def enter_license_plate(bdd_driver, licensePlateNum):
    autoquote_enter_license_plate(bdd_driver, licensePlateNum)


@when("I enter <annualMileage> value in annual mileage text box")
def enter_annual_mileage(bdd_driver, annualMileage):
    autoquote_enter_annual_mileage(bdd_driver, annualMileage)
