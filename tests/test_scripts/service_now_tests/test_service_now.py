import sys
import pytest
from config import TestConfig as config

sys.path.append("../../../")
from business_components.web_components.app_service_now import *
import logging

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
from utilities.helper import *
from PyAuto.PyAutoReadWrite import ReadWrite


@pytest.mark.web_healing_test
def test_service_now_incident_form(driver):
    fill_new_incident_form(driver, "admin", "v8DAe8EBHbym", "Self healing Demo")



