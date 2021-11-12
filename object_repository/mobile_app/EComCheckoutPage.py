import time

from selenium.webdriver.common.by import By

from PyAuto.PyAutoMobile import PyAutoMobile
from config import TestConfig as config


class EComCheckout(PyAutoMobile):
    locatorCartIcon = [(By.ID, "btn_add_cart")]
    locatorCheckoutButton = [(By.ID, "btn_checkout")]
    locatorNameTextbox = [(By.ID, "edt_name")]
    locatorShippingDropdown = [(By.ID, "spinner")]
    locatorUPS = [(By.XPATH, "//*[@text='UPS']")]
    locatorCommentTextBox = [(By.ID, "edt_comment")]
    locatorSubmitCheckout = [(By.ID, "btn_submit_order")]
    locatorYesButton = [(By.ID, "button1")]
    locatorWaitMessage = [(By.XPATH, "//*[@text='Submit your order…']")]
    locatorSuccessPopUp = [(By.ID, "alertTitle")]

    def __init__(self, mob_conn):
        super().__init__(mob_conn)  # call super class constructor
        self.mob_conn = mob_conn

    def navigate_to_cart(self):
        time.sleep(3)
        self.wait_mobile_element_visibility(self.locatorCartIcon)
        self.find_mobile_element_and_click(self.locatorCartIcon)
        return self

    def navigate_to_checkout(self):
        self.find_mobile_element_and_click(self.locatorCheckoutButton)
        return self

    def enter_name(self, name):
        self.wait_mobile_element_visibility(self.locatorNameTextbox)
        self.clear_mobile_element_text(self.locatorNameTextbox)
        self.enter_text_in_mobile_element(name, self.locatorNameTextbox)
        return self

    def select_shipping(self):
        self.find_mobile_element_and_click(self.locatorShippingDropdown)
        self.wait_mobile_element_visibility(self.locatorUPS)
        self.find_mobile_element_and_click(self.locatorUPS)
        return self

    def fill_comment(self, comment):
        self.swipe_from_coordinates(445, 1000, 445, 500)
        self.wait_mobile_element_visibility(self.locatorCommentTextBox)
        self.clear_mobile_element_text(self.locatorCommentTextBox)
        self.enter_text_in_mobile_element(comment, self.locatorCommentTextBox)
        return self

    def click_submit(self):
        self.find_mobile_element_and_click(self.locatorSubmitCheckout)
        time.sleep(2)
        return self

    def click_on_yes(self):
        self.wait_mobile_element_visibility(self.locatorYesButton)
        self.find_mobile_element_and_click(self.locatorYesButton)
        return self

    def wait_for_confirm(self):
        self.wait_mobile_element_visibility(self.locatorWaitMessage)
        self.wait_mobile_element_invisible(self.locatorWaitMessage)
        return self

    def assert_success_message(self):
        time.sleep(2)
        assert 'Congratulation' == self.get_text_from_mobile_element(self.locatorSuccessPopUp)
        self.close_current_app()
        return self
