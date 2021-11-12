from PyAuto.PyAutoLogger import get_logger
from object_repository.mobile_app.FlipkartHomePage import FlipkartHome
from object_repository.mobile_app.FlipkartHomeiOS import FlipkartHomeiOS
import allure
from PyAuto.PyAutoMobile import PyAutoMobile

logger = get_logger()


# -------------------------------- Android -------------------------------------------------
@allure.step("Search for Iphone 12")
def search_iphone(mob_conn):
    FlipkartHome(mob_conn).search_for_iphone().click_on_blue_iphone().get_price()


@allure.step("Swipe on image")
def scroll_iphone_image(mob_conn):
    FlipkartHome(mob_conn).search_for_iphone().click_on_blue_iphone().scroll_down()


# ----------------------------------- iOS ---------------------------------------------------
@allure.step("Search for item")
def search_product(mob_conn):
    FlipkartHomeiOS(mob_conn).search_for_iphone().get_price()


@allure.step("Open Flipkart and Go to Home")
def test_home_from_flipkart(mob_conn):
    FlipkartHomeiOS(mob_conn).search_for_iphone().goto_home().touch_hold_spotify().swipe_in_direction()
