import pytest

from business_components.desktop_components.windows_app_sap import *

import logging

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

@pytest.mark.sap_login
def test_sap_login(session):
    login_sap_session(session)

@pytest.mark.calc_addition
def test_calc_add(desktop_app):
    check_add_calc(desktop_app)


@pytest.mark.calc_addition
def test_calc_sq(desktop_app):
    check_sq_calc(desktop_app)