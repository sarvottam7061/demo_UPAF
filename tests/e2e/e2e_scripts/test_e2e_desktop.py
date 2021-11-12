import subprocess

import pytest
from business_components.desktop_components.windows_app_sap import *
from business_components.web_components.app_selenium_easy import *
from config import TestConfig as config


# you can call the test function directly as a test step in e2e tests

@pytest.mark.e2e_desktop
def test_e2e_desktop(desktop_app, driver):
    # if config.desktop_engine == "winappdriver":
    #     server = subprocess.Popen(config.winapp_server_path)
    # checkout_order_pos(desktop_app, "2386418073626")
    # the_text_should_be(desktop_app, "Connection Parameters")
    the_text_should_be(desktop_app, "system Connection Parameters")
    download_progress(driver)


