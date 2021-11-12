from pytest_bdd import scenarios, given, when, then, parsers
import pytest
from selenium import webdriver
from object_repository.mobile_app.FlipkartHomeiOS import FlipkartHomeiOS

scenarios('../features/mobile_flipkart.feature')


@given("The flipkart app is open in mobile and click Search")
def flipkart_open(mobile_conn):
    FlipkartHomeiOS(mobile_conn).search_for_iphone()


@then("Go back and Navigate to home")
def search_for_item(mobile_conn):
    FlipkartHomeiOS(mobile_conn).goto_home()


@then("Check for press and hold on spotify icon")
def check_for_hold(mobile_conn):
    FlipkartHomeiOS(mobile_conn).touch_hold_spotify()
