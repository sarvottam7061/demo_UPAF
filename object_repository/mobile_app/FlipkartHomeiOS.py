import time

from selenium.webdriver.common.by import By

from PyAuto.PyAutoMobile import PyAutoMobile
from config import TestConfig as config


class FlipkartHomeiOS(PyAutoMobile):
    locatorSearchTextbox = [(By.ID, "Search for Products, Brands and More")]
    # locatorSearchTextbox = [(By.XPATH, "//XCUIElementTypeOther[@id='Search for Products, Brands and More']")]
    locatorSearchBar = [(By.XPATH, "//*[@placeholder='Search for products and brands']")]
    locatorIphone12proSearchResult = [(By.XPATH, "//*[@id='iphone 12 pro']")]
    locatorIphone12pro = [(By.XPATH, "//*[contains(@id, 'APPLE iPhone 12 Pro (Gold, 128 GB)')]")]
    locatorIphonePrice = [(By.XPATH, "//*[contains(@id, '1,19,900')]")]
    locatorSpotifyIcon = [(By.XPATH, "//*[@id='Spotify']")]
    locatorPicIphone = [(By.XPATH, "(//*[@class='UIAView' and ./parent::*[@class='UIAScrollView' and ./parent::*[(./preceding-sibling::* | ./following-sibling::*)[./*[./*[./*[@class='UIAView']]]]]]]/*/*/*[@class='UIAView' and ./parent::*[@class='UIAView' and ./parent::*[@class='UIAView']]])[2]")]

    def __init__(self, mob_conn):
        super().__init__(mob_conn)  # call super class constructor
        self.mob_conn = mob_conn

    def search_for_iphone(self):
        self.wait_mobile_element_visibility(self.locatorSearchTextbox)
        self.find_mobile_element_and_click(self.locatorSearchTextbox)
        self.enter_text_in_mobile_element("iphone 12", self.locatorSearchBar)
        time.sleep(3)
        # self.wait_mobile_element_visibility(self.locatorIphone12proSearchResult)
        self.find_mobile_element_and_click(self.locatorIphone12proSearchResult)
        self.find_mobile_element_and_click(self.locatorIphone12pro)
        time.sleep(3)
        return self

    def get_price(self):
        self.swipe_from_coordinates(100, 966, 100, 700)
        time.sleep(3)
        print(self.get_text_from_mobile_element(self.locatorIphonePrice))
        return self

    def goto_home(self):
        self.go_back_mobile()
        self.navigate_home_mobile()
        return self

    def touch_hold_spotify(self):
        spotify_element = self.find_mobile_element_from_list_wait(self.locatorSpotifyIcon)
        self.touch_and_hold_element(spotify_element)
        return self

    def swipe_in_direction(self):
        self.mobile_swipe_from_direction(direction='right')
        return self
