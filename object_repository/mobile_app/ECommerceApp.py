import time

from selenium.webdriver.common.by import By

from PyAuto.PyAutoMobile import PyAutoMobile
from config import TestConfig as config


class HealthSports(PyAutoMobile):
    locatorCategoryButton = [(By.ID, "nav_category")]
    locatorHealthSports = [(By.XPATH, "//*[@text='Health & Sports']")]
    locatorNikeShoe = [(By.XPATH, "//*[@text='Nike Magista Obra II Club TF']")]
    locatorPrice = [(By.XPATH, "//*[@text='42 USD']")]
    locatorAddCart = [(By.ID, "btn_add_cart")]
    locatorQuantityTextbox = [(By.ID, "userInputDialog")]
    locatorAddButton = [(By.XPATH, "//*[@text='ADD']")]

    def __init__(self, mob_conn):
        super().__init__(mob_conn)  # call super class constructor
        self.mob_conn = mob_conn

    def navigate_to_shoe(self):
        time.sleep(3)
        self.find_mobile_element_and_click(self.locatorCategoryButton)
        self.find_mobile_element_and_click(self.locatorHealthSports)
        self.find_mobile_element_and_click(self.locatorNikeShoe)
        return self

    def validate_price_of_shoe(self):
        shoe_element = self.find_mobile_element_from_list_wait(self.locatorPrice, wait_time=3)
        assert self.get_text_from_mobile_element(shoe_element) == "42 USD"
        return self

    def click_add_cart(self):
        self.find_mobile_element_and_click(self.locatorAddCart)
        return self

    def enter_quantity(self, quantity):
        self.enter_text_in_mobile_element(quantity, self.locatorQuantityTextbox)
        return self

    def click_on_add(self):
        self.find_mobile_element_and_click(self.locatorAddButton)
        self.close_current_app()
        return self
