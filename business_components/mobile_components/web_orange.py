import allure
from object_repository.mobile_web.AppInpuForm import InputFormMobile
from object_repository.mobile_web.AppInpuFormIos import InputFormMobileIos
from config import TestConfig as config


@allure.step("Web app testing ios")
def ios_web_SeleniumEasy(mob_conn):
    mob_conn.get(config.mobile_web_url)
    InputFormMobileIos(mob_conn).navigate().enter_fname("Prateek").enter_lname("Das").enter_phone("123456").enter_address("I live here").enter_city("City").select_state("Alaska").radio_hosting("yes").click_send()
    # InputFormMobile(mob_conn).navigate().enter_fname("Prateek").enter_lname("Das").enter_phone("123456").enter_address("I live here").enter_city("City").radio_hosting("yes")


@allure.step("Web app testing Android")
def android_web_SeleniumEasy(mob_conn):
    mob_conn.get(config.mobile_web_url)

    # InputFormMobile(mob_conn).navigate()#.set_context_to("WEBVIEW_1").enter_fname("Prateek")
    # InputFormMobile(mob_conn).navigate().enter_fname("Prateek")
    InputFormMobile(mob_conn).navigate().enter_fname("Prateek")
