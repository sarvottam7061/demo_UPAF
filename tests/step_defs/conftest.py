import traceback

import appium
import pytest
import sys
import allure
import datetime
import json
sys.path.append("../../")
from allure_commons.types import AttachmentType
from PyAuto.PyAutoException import handle_selenium_exception, PyAutoExceptions
from PyAuto.PyAutoLogger import get_logger
import pickle
import os
from selenium.webdriver import DesiredCapabilities

from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from config import TestConfig as config

import logging
import allure
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

logger = get_logger()


# To forward the logs to allure report
class AllureLoggingHandler(logging.Handler):
    def log(self, message):
        with allure.step('Log {}'.format(message)):
            pass

    def emit(self, record):
        self.log("({}) {}".format(record.levelname, record.getMessage()))


# To forward the logs to allure report
class AllureCatchLogs:
    def __init__(self):
        self.rootlogger = logging.getLogger()
        self.allurehandler = AllureLoggingHandler()

    def __enter__(self):
        if self.allurehandler not in self.rootlogger.handlers:
            self.rootlogger.addHandler(self.allurehandler)

    def __exit__(self, exc_type, exc_value, traceback):
        self.rootlogger.removeHandler(self.allurehandler)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup():
    with AllureCatchLogs():
        yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call():
    with AllureCatchLogs():
        yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown():
    with AllureCatchLogs():
        yield
        




@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    pytest_html = None
    if rep.when == 'call' and rep.failed:
        if config.analyze_failures:
            now_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            if os.path.isfile(failure_analysis_file):
                with open(failure_analysis_file, "r+") as file:
                    data = json.load(file)
                    data[str(os.environ.get('PYTEST_CURRENT_TEST')).split(" (call)")[
                        0]] = [call.excinfo._getreprcrash().message, now_time]
                    file.seek(0)
                    json.dump(data, file, indent=4)
            else:
                data = {
                    str(os.environ.get('PYTEST_CURRENT_TEST').split(" (call)")[0]): [call.excinfo._getreprcrash().message, now_time]}
                with open(failure_analysis_file, "w") as file:
                    json.dump(data, file, indent=4)
            
      


# driver instance variable - global scope
d = None

# Get browser value from a pickle file

run_config_file = os.path.abspath('../../resources/run_time_config.pkl')
with open(run_config_file, 'rb') as file:
    # A new file will be created
    run_config = pickle.load(file)

browser_value = run_config['browser']
exec_type = run_config['exec_type']
test_url = run_config['bdd_url']
url = test_url
failure_analysis_path = run_config['failure_analysis']
failure_analysis_file = failure_analysis_path + "/failures.json"


# initialize browser in selenium bdd module
def pytest_bdd_before_scenario(request, feature, scenario):
    """Called before scenario is executed."""
    global d
    browser = browser_value.lower()
    try:
        if browser == "chrome":
            chrome_options = webdriver.ChromeOptions()
            for option in config.chromeOptions[exec_type]:
                chrome_options.add_argument(option)
            if config.manage_driver:
                d = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
            else:
                d = webdriver.Chrome(executable_path=config.chrome_driver, options=chrome_options)
        elif browser == "firefox":
            firefox_options = webdriver.FirefoxOptions()
            for option in config.fireFoxOptions[exec_type]:
                firefox_options.add_argument(option)
            if config.manage_driver:
                d = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)
            else:
                d = webdriver.Firefox(executable_path=config.gecko_driver, options=firefox_options)
        elif browser == "edge":
            edge_options = EdgeOptions()
            edge_options.use_chromium = True
            for option in config.edgeOptions[exec_type]:
                edge_options.add_argument(option)
            if config.manage_driver:
                d = Edge(executable_path=EdgeChromiumDriverManager().install(), options=edge_options)
            else:
                d = Edge(executable_path=config.edge_driver, options=edge_options)
        elif browser == "ie":
            ie_options = webdriver.IeOptions()
            for option in config.IEOptions[exec_type]:
                ie_options.add_argument(option)
            if config.manage_driver:
                d = webdriver.Ie(executable_path=IEDriverManager().install(), options=ie_options)
            else:
                d = webdriver.Ie(executable_path=config.ie_driver, options=ie_options)
        elif browser == "safari":
            d = webdriver.Safari(executable_path=config.safari_driver)
        elif browser == "remote":
            d = webdriver.Remote(command_executor=config.remoteOptions['url'],
                                 desired_capabilities=config.desiredCapabilities_remote)
        else:
            logger.error(config.browser + "Browser is not supported, Launching the test in chrome")
            d = webdriver.Chrome(config.chrome_driver)
        d.maximize_window()
        d.get(url)
        d.implicitly_wait(config.implicit_wait)
    except Exception as E:
        handle_selenium_exception(E)
    if d is None:
        raise PyAutoExceptions(config.browser + " Browser instantiation failed. check error logs for more info")


# bdd driver after completion of scenario
def pytest_bdd_after_scenario(request, feature, scenario):
    global d
    d.quit()
    """Called after scenario is executed."""


# attach screenshot after a failed step completion
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    global d
    html_button = '''
                      <center><a href="failed.html" target="_blank"> <button style="background-color: #B22222; text-align: center; color: White;font-size: 23px;padding: 8px;border: none;margin: 50px;width: 50%;">Report </button></a></center>
                      '''
    allure.attach(html_button, "Failure Analysis",
                  allure.attachment_type.HTML)
    allure.attach(d.get_screenshot_as_png(), name="failedStep", attachment_type=AttachmentType.PNG)


# to call bdd driver in your test steps
@pytest.fixture
def bdd_driver():
    global d
    yield d


mob_conn = None
# pytest fixture for Mobile Testing, the function name when called in your test
@pytest.fixture
def mobile_conn():
    global mob_conn
    try:
        mob_conn = appium.webdriver.Remote(config.mob_remote_url, config.desiredCapabilities_mobile)
    except:
        if config.desiredCapabilities_mobile['appPackage']:
            config.desiredCapabilities_mobile['app'] = config.mobile_apk_path
            mob_conn = appium.webdriver.Remote(config.mob_remote_url, config.desiredCapabilities_mobile)
        elif config.desiredCapabilities_mobile['bundleId']:
            config.desiredCapabilities_mobile['app'] = config.mobile_ipa_path
            mob_conn = appium.webdriver.Remote(config.mob_remote_url, config.desiredCapabilities_mobile)
        elif config.desiredCapabilities_mobile['browserName']:
            raise Exception(f"Error in launching the browser {config.desiredCapabilities_mobile['browserName']}.")
    yield mob_conn
    mob_conn.quit()
