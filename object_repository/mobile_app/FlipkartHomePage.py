import time

from selenium.webdriver.common.by import By

from PyAuto.PyAutoMobile import PyAutoMobile
from config import TestConfig as config


class FlipkartHome(PyAutoMobile):
    locatorSearchTextbox = [(By.ID, "search_widget_textbox")]
    locatorLanguage = [(By.XPATH, "//*[@text='English']")]
    locatorLanguageContinue = [(By.ID, "select_btn")]
    locatorBackButton = [(By.ID, "custom_back_icon")]
    locatorSearchBar = [(By.ID, "search_autoCompleteTextView")]
    locatorIphone12SearchResult = [(By.XPATH, "//*[@text='iphone 12']")]
    locatorBlueIphone12 = [(By.XPATH, "//*[@text='APPLE iPhone 12 (Black, 128 GB)']")]
    locatorIphonePrice = [(By.XPATH, "//*[@text='₹71,999']")]

    def __init__(self, mob_conn):
        super().__init__(mob_conn)  # call super class constructor
        self.mob_conn = mob_conn

    def close_popup(self):
        self.find_mobile_element_and_click(self.locatorLanguage)
        self.find_mobile_element_and_click(self.locatorLanguageContinue)
        time.sleep(3)
        self.go_back_mobile()
        self.find_mobile_element_and_click(self.locatorBackButton)
        return self

    def search_for_iphone(self):
        # self.close_popup()
        self.wait_mobile_element_visibility(self.locatorSearchTextbox)
        self.find_mobile_element_and_click(self.locatorSearchTextbox)
        self.enter_text_in_mobile_element("iphone", self.locatorSearchBar)
        time.sleep(3)
        self.wait_mobile_element_visibility(self.locatorIphone12SearchResult)
        self.find_mobile_element_and_click(self.locatorIphone12SearchResult)
        return self

    def click_on_blue_iphone(self):
        self.find_mobile_element_and_click(self.locatorBlueIphone12)
        time.sleep(3)
        return self

    def get_price(self):
        time.sleep(3)
        self.scroll_down()
        price_element = self.find_mobile_element_from_list_wait(self.locatorIphonePrice)
        price = self.get_text_from_mobile_element(price_element)
        self.set_text_to_clipboard(price)
        price_from_cb = self.get_text_from_clipboard()
        print(price_from_cb)
        return self

    def session_capabilities(self):
        return self.get_session_capabilities()

    def scroll_down(self):
        self.swipe_from_coordinates(445, 1000, 445, 500)
        return self




