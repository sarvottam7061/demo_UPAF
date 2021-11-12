import allure
from pywinauto.timings import Timings

from PyAuto.PyAutoLogger import get_logger
from object_repository.screens.Calculator import Calc
from object_repository.screens.SapGuiAuto import SapGuiPom

logger = get_logger()

@allure.step("addition in calc")
def check_add_calc(app):
    Calc(app).addition()


@allure.step("square in calc")
def check_sq_calc(app):
    Calc(app).square()

def login_sap_session(session):
    SapGuiPom(
        session).open_connection().login_sap().enter_tcode().create_sales_doc().create_standard_order()\
        .display_header_details().get_doc_complete().save_and_get_order_number()
