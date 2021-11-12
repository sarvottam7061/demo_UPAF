from object_repository.pages.ServiceNowIncident import IncidentForm

from PyAuto.PyAutoLogger import get_logger

import allure

logger = get_logger()


# Use method chaining by creating an object from the page name
@allure.step("Create and Submit new Incident")
def fill_new_incident_form(driver, username, password, desc):
    IncidentForm(driver).get_inside_iframe1().enter_username(username).enter_password(password)\
        .click_login().click_incident().get_inside_iframe2().click_new_incident()\
        .enter_description(desc).click_submit()



