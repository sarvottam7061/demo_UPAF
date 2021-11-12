from PyAuto.PyAutoLogger import get_logger
from object_repository.mobile_app.ECommerceApp import HealthSports
from object_repository.mobile_app.EComCheckoutPage import EComCheckout
import allure

logger = get_logger()


@allure.step("Validate price of the shoe")
def validate_shoe_price(mob_conn):
    HealthSports(mob_conn).navigate_to_shoe().validate_price_of_shoe()


@allure.step("Add to Cart")
def add_to_cart(mob_conn, quantity):
    HealthSports(mob_conn).click_add_cart().enter_quantity(quantity).click_on_add()


@allure.step("Fill checkout form")
def checkout_form_fillup(mob_conn, name, comment):
    EComCheckout(mob_conn).navigate_to_cart().navigate_to_checkout().enter_name(name).select_shipping().fill_comment(comment).click_submit().click_on_yes().wait_for_confirm().assert_success_message()
