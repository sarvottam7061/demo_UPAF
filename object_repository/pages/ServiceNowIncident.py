from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb
from selenium.webdriver.support.select import Select
from PyAuto.PyAutoHeal import class_attributes
from config import TestConfig as config
import pdb


class IncidentForm(PyAutoWeb):
    # Define all the locators here. Multiple locator strategy is used,
    # if any one locator fails, framework will take up next in the list
    locatorUsername = [(By.NAME, "user_name"), (By.XPATH, '//*[@id="user_name"]'),
                       (By.ID, "user_name")]
    locatorPassword = [(By.NAME, "user_password"), (By.XPATH, '//*[@id="user_password"]'),
                       (By.ID, "user_password")]
    locatorLogin = [(By.NAME, "not_important"), (By.XPATH, '//*[@id="sysverb_login"]"]'),
                    (By.ID, "sysverb_login")]
    locatorIncidents = [(By.TAG_NAME, "Incidents"), (By.XPATH, '//*[@id="087800c1c0a80164004e32c8a64a97c9"]/div/div')]

    locatorNewIncident = [(By.ID, "sysverb_new")]

    locatorDescription = [(By.XPATH, '//*[@id="incident.short_description"]'),
                    (By.ID, "incident.short_description")]
    locatorSubmit = [(By.NAME, "not_important"), (By.XPATH, '//*[@id="sysverb_insert_bottom"]'),
                    (By.ID, "sysverb_insert_bottom")]
    locatorIframe1 = [(By.ID, "gsft_main")]
    locatorIframe2 = [(By.ID, "gsft_main")]
    def __init__(self, driver, url=""):
        super().__init__(driver)  # call super class constructor
        if config.run_mode == 'capture' or config.run_mode == 'capture&heal':
            class_attributes(self)
        self.driver = driver
        # if you create an object with url, it will validate the url for current page
        self.url = driver.current_url if url == "" else url
        if driver.current_url != self.url:
            self.driver.get(self.url)

    # methods to perform operation in the page following page object model
    def get_inside_iframe1(self,):
        self.wait_switch_to_frame(self.locatorIframe1)
        return self

    def enter_username(self, uname):
        self.enter_text(uname, self.locatorUsername, waitStrategy="clickable")
        # self.wait(4)
        return self

    def enter_password(self, pwd):
        # pdb.set_trace()
        self.enter_text(pwd, self.locatorPassword)
        return self

    def click_login(self):
        # self.wait(4)
        self.click_wait_locator(self.locatorLogin)
        return self

    def click_incident(self):
        self.click_wait_locator(self.locatorIncidents)
        return self

    def get_inside_iframe2(self):
        self.wait_switch_to_frame(self.locatorIframe2)
        return self

    def click_new_incident(self):
        self.click_wait_locator(self.locatorNewIncident)
        return self


    def enter_description(self, desc):
        pdb.set_trace()
        self.enter_text(desc, self.locatorDescription, waitStrategy="clickable")
        self.wait(4)
        return self

    def click_submit(self):
        self.click_wait_locator(self.locatorSubmit)
        return self


