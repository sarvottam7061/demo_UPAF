import time

import pytest
import logging


from selenium.webdriver.common.by import By
from config import TestConfig as config
from PyAuto.PyAutoSelenium import PyAutoWeb
from object_repository.mobile_web.AppInpuForm import InputFormMobile
from business_components.mobile_components.app_ecommerce import *
from business_components.mobile_components.app_flipkart import *
from business_components.mobile_components.web_orange import *

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

locatorUserName = [(By.ID, 'txtUsername')]


@pytest.mark.open_youtube
def test_mobile_youtube(mobile_conn):
    mobile_conn.find_element_by_xpath("//*[@text='YouTube']").click()
    # mobile_conn.startActivity("Youtube", "")
    time.sleep(5)
    mobile_conn.find_element_by_xpath("//*[@id='menu_item_1']").click()
    time.sleep(3)
    mobile_conn.find_element_by_xpath("//*[@id='search_edit_text']").send_keys('Appium')
    mobile_conn.execute_script("seetest:client.sendText(\"{ENTER}\")")
    time.sleep(5)


@pytest.mark.clear_open_apps
def test_clear_open_apps(mobile_conn):
    mobile_conn.press_keycode(187)  # recent apps
    mobile_conn.execute_script("seetest:client.swipe(\"Up\", 100, 500)")
    mobile_conn.find_element_by_xpath("//*[@text='CLEAR ALL']").click()


@pytest.mark.web_mobile
def test_browser(mobile_conn):
    mobile_conn.get("https://opensource-demo.orangehrmlive.com/")
    time.sleep(3)
    mobile_conn.find_element_by_id('txtUsername')
    # pwd_textbox = mobile_conn.find_element_by_id('txtPassword')
    # pwd_textbox.send_keys('Admin')
    # sub_btn = mobile_conn.find_element_by_id('btnLogin')
    # sub_btn.click()
    time.sleep(3)


@pytest.mark.demoTest_native
def test_verify_price(mobile_conn):
    # mobile_conn.install_app("C:\\Users\\ASUS\\Downloads\\apk_mob\\ECommerce_Demo_v3.apk")
    # mobile_conn.start_activity("com.solodroid.solomerce", "com.solodroid.solomerce.activities.ActivitySplash")
    # nav_button = mobile_conn.find_element_by_xpath("//*[@id='nav_category']")
    # nav_button.click()
    # locatorCategoryButton = "//*[@id='nav_category']"
    # PyAutoMobile(mobile_conn).find_element_and_click(locatorCategoryButton)
    locatorCategoryButton = [(By.ID, "nav_category")]
    locatorHealthSports = [(By.XPATH, "//*[@text='Health & Sports']")]
    locatorNikeShoe = [(By.XPATH, "//*[@text='Nike Magista Obra II Club TF']")]
    locatorPrice = [(By.XPATH, "//*[@text='42 USD']")]

    shoe_element = PyAutoMobile(mobile_conn).find_mobile_element_and_click(locatorCategoryButton).find_element_and_click(
        locatorHealthSports).find_element_and_click(locatorNikeShoe).find_element_from_list_wait(locatorPrice)
    time.sleep(3)
    cost_shoe = PyAutoMobile(mobile_conn).get_text_from_mobile_element(shoe_element)
    assert cost_shoe == "42 USD"


@pytest.mark.mobile_orange
def test_orange(mobile_conn):
    locatorUsernameTextbox = [(By.ID, "txtUsername")]
    locatorPasswordTextbox = [(By.ID, "txtPassword")]
    locatorLoginButton = [(By.ID, "btnLogin")]
    locatorInfoTab = [(By.ID, "menu_pim_viewMyDetails")]
    locatorFirstName = [(By.ID, "personal_txtEmpFirstName")]
    locatorBloodGroup = [(By.ID, "btnEditCustom")]
    locatorBloodGroupDrpDown = [(By.NAME, "custom1")]

    mobile_conn.get("https://opensource-demo.orangehrmlive.com/")
    mobile_conn.switch_to.context("NATIVE_APP")
    PyAutoWeb(mobile_conn).find_element_from_list_wait(locatorUsernameTextbox).clear()

    name_webElement = PyAutoWeb(mobile_conn).enter_text('Admin', locatorUsernameTextbox).enter_text('admin123',
                                                                                                    locatorPasswordTextbox) \
        .click_wait_locator(locatorLoginButton).click_wait_locator(locatorInfoTab).wait_element_visibility(
        locatorFirstName) \
        .find_element_from_list_wait(locatorFirstName)
    first_name = PyAutoWeb(mobile_conn).get_element_text(name_webElement)
    print(first_name)
    # PyAutoWeb(mobile_conn).click_wait_locator(locatorBloodGroup)
    # time.sleep(2)
    # PyAutoWeb(mobile_conn).select_element_value(locatorBloodGroupDrpDown, "A+").click_wait_locator(locatorBloodGroup)


@pytest.mark.mobile_orange_test2
def test_orange_2(mobile_conn):
    locatorUsernameTextbox = [(By.ID, "txtUsername")]
    locatorPasswordTextbox = [(By.ID, "txtPassword")]
    locatorLoginButton = [(By.ID, "btnLogin")]
    locatorAdminTab = [(By.ID, "menu_admin_viewAdminModule")]
    locatorMenuOption = [(By.ID, "menu_admin_Job")]
    locatorJobTitles = [(By.ID, "menu_admin_viewJobTitleList")]
    locatorAlljobs = [(By.XPATH, "//*[@id='resultTable']/tbody/tr")]

    mobile_conn.get("https://opensource-demo.orangehrmlive.com/")
    mobile_conn.switch_to.context("NATIVE_APP")

    PyAutoWeb(mobile_conn).enter_text('Admin', locatorUsernameTextbox).enter_text('admin123',locatorPasswordTextbox) \
        .click_wait_locator(locatorLoginButton).click_wait_locator(locatorAdminTab).click_wait_locator(locatorMenuOption).click_wait_locator(locatorJobTitles)
    time.sleep(3)
    jobs = PyAutoWeb(mobile_conn).find_elements_from_list(locatorAlljobs)
    print(len(jobs))


@pytest.mark.mobile_selenium_easy
def test_selenium_easy(mobile_conn):
    android_web_SeleniumEasy(mobile_conn)
    # mobile_conn.get(config.mobile_web_url)
    # InputFormMobile(mobile_conn).navigate()
    # mobile_conn.switch_to.context("WEBVIEW_1")
    # mobile_conn.switch_to.context("NATIVE_APP")
    # InputFormMobile(mobile_conn).enter_fname("Prateek")


@pytest.mark.perform_actions
def test_actions(mobile_conn):
    locatorCategoryButton = [(By.ID, "nav_category")]
    locatorHealthSports = [(By.XPATH, "//*[@text='Health & Sports']")]
    locatorNikeShoe = [(By.XPATH, "//*[@text='Nike Magista Obra II Club TF']")]

    PyAutoMobile(mobile_conn).find_mobile_element_and_click(locatorCategoryButton).find_element_and_click(locatorHealthSports)
    time.sleep(3)
    # print(PyAutoMobile(mobile_conn).get_app_status('com.solodroid.solomerce'))
    print(PyAutoMobile(mobile_conn).get_element_location_mobile(locatorNikeShoe))
    print(PyAutoMobile(mobile_conn).get_element_size_mobile(locatorNikeShoe))


@pytest.mark.nike_shoe_test
def test_validate_price(mobile_conn):
    validate_shoe_price(mobile_conn)
    add_to_cart(mobile_conn, quantity=4)


@pytest.mark.checkout_test
def test_checkout_complete(mobile_conn):
    checkout_form_fillup(mobile_conn, "Prateek Das", "A Sample Comment")


@pytest.mark.flipkart_search_iphone
def test_flipkart_search(mobile_conn):
    search_iphone(mobile_conn)


@pytest.mark.swipe_image
def test_swipe_image(mobile_conn):
    scroll_iphone_image(mobile_conn)


@pytest.mark.test_flipkart_ios
def test_search_for_iphone(mobile_conn):
    search_product(mobile_conn)


@pytest.mark.test_ios_web
def test_orange_ios(mobile_conn):
    ios_web_SeleniumEasy(mobile_conn)


@pytest.mark.test_home
def test_nav_home(mobile_conn):
    test_home_from_flipkart(mobile_conn)

