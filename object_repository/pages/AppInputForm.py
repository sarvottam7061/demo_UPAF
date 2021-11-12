from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb
from selenium.webdriver.support.select import Select
from PyAuto.PyAutoHeal import class_attributes
from config import TestConfig as config
import pdb


class InputForm(PyAutoWeb):

    # Define all the locators here. Multiple locator strategy is used,
    # if any one locator fails, framework will take up next in the list
    locatorFnameText = [(By.NAME, "first_name"), (By.XPATH, "//input[@data-bv-field='first_name']"),
                        (By.CSS_SELECTOR, "input[placeholder='First Name']")]
    locatorLnameText = [(By.NAME, "last_name")]
    locatorLname_except = [(By.NAME, "last_nae"), (By.CSS_SELECTOR, "input[placeholder='Lasame']"), (By.ID, "last_")]
    locatorEmailText = [(By.NAME, "email"), (By.XPATH, "//input[@data-bv-field='email']")]
    locatorPhoneText = [(By.NAME, "phone")]
    locatorAddressText = [(By.NAME, "address"), (By.CSS_SELECTOR, "input[placeholder='Address']"),
                          (By.XPATH, "//input[@data-bv-field='address']")]
    locatorCityText = [(By.NAME, "city")]
    locatorStateDrp = [(By.NAME, "state")]  
    locatorZipText = [(By.NAME, "zip")]
    locatorWebsiteText = [(By.NAME, "website")]
    locatorHostingYesRadio = [(By.XPATH, "//label/input[@value='yes']")]
    locatorHostingNoRadio = [(By.XPATH, "//label/input[@value='no']")]
    locatorProjectDescText = [(By.NAME, "comment")]
    locatorButtonSend = [(By.XPATH, "(//button[@type='submit'])[2]")]
    locatorInputFormNav = [(By.PARTIAL_LINK_TEXT, "Input Forms")]
    locatorInputFormSubMenu = [(By.LINK_TEXT, "Input Form Submit")]
    locatorClosePopupBtnLink = [(By.LINK_TEXT, "No, thanks!")]


    def __init__(self, driver, url=""):
        super().__init__(driver)# call super class constructor
        if config.run_mode == 'capture' or config.run_mode=='capture&heal':
            class_attributes(self)
        self.driver = driver
        # if you create an object with url, it will validate the url for current page
        self.url = driver.current_url if url == "" else url
        if driver.current_url != self.url:
            self.driver.get(self.url)

    #methods to perform operation in the page following page object model
    def enter_fname(self, fname):
        self.enter_text(fname, self.locatorFnameText, waitStrategy="clickable")
        return self

    def enter_lname(self, lname):
        # pdb.set_trace()
        self.enter_text(lname, self.locatorLnameText)
        return self

    def enter_lname_except(self, lname):
        web_element = self.find_element_from_list_wait(self.locatorLname_except)
        web_element.send_keys(lname)
        return self

    def enter_email(self, email):
        self.enter_text(email, self.locatorEmailText, wait_time=2, waitStrategy="visibility")
        return self

    def enter_phone(self, phone):
        self.enter_text(phone, self.locatorPhoneText)
        return self

    def enter_address(self, address):
        self.enter_text(address, self.locatorAddressText)
        return self

    def enter_city(self, city):
        self.enter_text(city, self.locatorCityText)
        return self

    def select_state(self, state):
        stateDrpDown = self.find_element_from_list_wait(self.locatorStateDrp)
        Select(stateDrpDown).select_by_visible_text(state)
        return self

    def enter_zip(self, zip_code):
        self.enter_text(zip_code, self.locatorZipText)
        return self

    def enter_web(self, website):
        self.enter_text(website, self.locatorWebsiteText)
        return self

    def radio_hosting(self, hosting):
        if hosting == "yes":
            hostRadio = self.find_element_from_list(self.locatorHostingYesRadio)
        else:
            hostRadio = self.find_element_from_list(self.locatorHostingNoRadio)
        hostRadio.click()
        return self

    def enter_desc(self, project_desc):
        self.enter_text(project_desc, self.locatorProjectDescText)
        return self

    def click_send(self):
        self.click_wait_locator(self.locatorButtonSend)
        self.wait(2)
        return self

    def close_pop(self):
        self.click_wait_locator(self.locatorClosePopupBtnLink)
        return self

    def navigate(self):
        self.close_pop()
        self.click_wait_locator(self.locatorInputFormNav)
        self.click_wait_locator(self.locatorInputFormSubMenu)
        self.wait(2)
        return self

    def validate_element_enabled(self):
        self.element_should_be_enabled(self.locatorHostingYesRadio)
        return self

    def find_attributes_of_send_button(self):
        self.get_all_attributes(self.locatorButtonSend)
        return self

    def element_attribute_value_validation(self, attr, attr_value):
        # web_element = self.find_element_from_list(self.locatorHostingYesRadio)
        self.element_attribute_value_should_be(self.find_element_from_list(self.locatorHostingYesRadio), attr, attr_value)
        return self

