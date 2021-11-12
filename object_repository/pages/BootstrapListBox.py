from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb


class ListBox(PyAutoWeb):
    # Define all the locators here. Multiple locator strategy is used,
    # if any one locator fails, framework will take up next in the list
    locatorSearchBox = [(By.NAME, "SearchDualList"), (By.XPATH, "//*[@id='listhead']/div[1]/div/input"),
                        (By.CSS_SELECTOR, "input[placeholder='search']")]
    locatorSearchResult = [(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div/ul/li[3]")]
    locatorMoveToList = [(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/button[2]")]
    locatorListBox = [(By.LINK_TEXT, "List Box")]
    locatorBootstrapListBox = [(By.LINK_TEXT, "Bootstrap List Box")]
    locatorClosePopupBtnLink = [(By.LINK_TEXT, "No, thanks!")]
    locatorNotVisible = [(By.LINK_TEXT, "Bootstrap List Box")]
    locatorCheckFocused = [(By.XPATH, "//*[@id='listhead']/div[1]/div/input")]
    locatorContainsFacilisis = [(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div/ul/li[2]")]
    locatorSearchIcon = [(By.XPATH, "//*[@id='listhead']/div[2]/div/span")]
    locatorClickable = [(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div/ul/li[1]")]
    locatorPresent = [(By.XPATH, "//li[contains(text(),'Cras justo odio')]")]
    locatorNotPresent = [(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[3]/div/ul/li[6]")]

    def __init__(self, driver, url=""):
        super().__init__(driver)  # call super class constructor
        self.driver = driver
        # if you create an object with url, it will validate the url for current page
        self.url = driver.current_url if url == "" else url
        if driver.current_url != self.url:
            self.driver.get(self.url)

    # methods to perform operation in the page following page object model
    def element_contains_fas(self, text):
        ele = self.find_element_from_list(self.locatorContainsFacilisis)
        self.element_should_contain(ele, text)
        return self

    def element_not_contains_fas(self, text):
        ele = self.find_element_from_list(self.locatorContainsFacilisis)
        self.element_should_not_contain(ele, text)
        return self

    def open_menu_at_search(self):
        ele = self.find_element_from_list(self.locatorSearchIcon)
        self.open_context_menu(ele)
        self.wait(3)
        return self

    def check_focused_element(self):
        self.click_wait_locator(self.locatorCheckFocused)
        self.element_should_be_focused(self.locatorCheckFocused)

    def search_list(self, text):
        self.enter_text(text, self.locatorSearchBox, waitStrategy="clickable")
        self.wait(3)
        return self

    def key_to_press(self, key_name):
        element = self.find_element_from_list(self.locatorSearchBox)
        self.press_key(element, key_name)
        self.wait(3)

    def select_list(self):
        self.click_wait_locator(self.locatorSearchResult)
        return self

    def move(self):
        self.click_wait_locator(self.locatorMoveToList)
        self.wait(3)
        return self

    def list_box_page_refresh(self):
        self.refresh_page()
        self.wait(3)
        return self

    def is_visible(self):
        # element = self.find_element_from_list_wait(self.locatorListBox)
        print("Is element visible: " + str(self.element_should_visible(self.locatorSearchBox)))
        # return self
        # # element = self.find_element_from_list_wait(self.locatorNotVisible, "presence")
        # print(self.element_should_visible(self.locatorNotVisible))
        return self

    def is_not_visible(self):
        print("is element not visible: " + str(self.element_should_not_visible(self.locatorNotVisible)))
        return self

    def element_clickable(self):
        self.wait_element_clickable(self.locatorClickable)
        self.wait(3)
        return self

    def element_present(self):
        self.wait_element_present(self.locatorPresent)
        self.wait(3)
        return self

    def element_not_present(self):
        self.wait_element_present(self.locatorNotPresent)
        self.wait(3)
        return self

    def close_pop(self):
        self.click_wait_locator(self.locatorClosePopupBtnLink)
        return self

    def navigate(self):
        self.close_pop()
        self.click_wait_locator(self.locatorListBox)
        self.click_wait_locator(self.locatorBootstrapListBox)
        self.wait(2)
        return self
