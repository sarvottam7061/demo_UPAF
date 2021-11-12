import datetime
import json
import subprocess
import time
import pytest
import sys
from pywinauto import Application, Desktop
from pywinauto.timings import Timings
sys.path.append("../../")
from allure_commons.types import AttachmentType
from PyAuto.PyAutoException import handle_selenium_exception, PyAutoExceptions
import logging
import pickle
from zeep import Client
from PyAuto.PyAutoRest import PyRest
from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from config import TestConfig as config
import os
from PyAuto.PyAutoLogger import get_logger
import allure
import appium
from sqlalchemy import create_engine
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


# driver instance variable - global scope
d = None

run_config_file = os.path.abspath('../../resources/run_time_config_e2e.pkl')
with open(run_config_file, 'rb') as file:
    # A new file will be created
    run_config = pickle.load(file)


# Before function to be used in selenium scripting module
def before_scenario():
    global d, run_config
    browser_value = run_config['browser']
    browser = browser_value.lower()
    url = run_config['web_url']
    exec_type = run_config['exec_type']
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


failure_analysis_path = run_config['failure_analysis']
failure_analysis_file = failure_analysis_path + "/failures.json"
# to attach screenshot for failed tests
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    global d, app, mob_conn
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
                    
        if config.ReportType == "allure" or config.ReportType == "both":
            if d and run_config['bdd'] == False:
                allure.attach(d.get_screenshot_as_png(),
                              name='screenshot',
                              attachment_type=allure.attachment_type.PNG)
            if mob_conn:
                allure.attach(mob_conn.get_screenshot_as_png(),
                              name='screenshot',
                              attachment_type=allure.attachment_type.PNG)   
            if run_config['bdd'] == False:
                html_button = '''
                            <center><a href="failed.html" target="_blank"> <button style="background-color: #B22222; text-align: center; color: White;font-size: 23px;padding: 8px;border: none;margin: 50px;width: 50%;">Report </button></a></center>
                            '''
                allure.attach(html_button, "Failure Analysis",
                              allure.attachment_type.HTML)
            pytest_html = item.config.pluginmanager.getplugin('html')
        report = outcome.get_result()
        extra = getattr(report, 'extra', [])
        if config.ReportType == "html" or config.ReportType == "both":
            if d:
                d.save_screenshot(config.screenshot_folder + "failed" + '.png')
                extra.append(pytest_html.extras.image(config.screenshot_folder + "failed" + '.png'))
                report.extra = extra
            if mob_conn:
                mob_conn.save_screenshot(config.screenshot_folder + "failed_mobile" + '.png')
                extra.append(pytest_html.extras.image(config.screenshot_folder + "failed_mobile" + '.png'))
                report.extra = extra

        if config.desktop_engine == "winappdriver":
            if config.ReportType == "allure" or "both":
                if app:
                    allure.attach(app.get_screenshot_as_png(),
                                  name='screenshot',
                                  attachment_type=allure.attachment_type.PNG)
                pytest_html = item.config.pluginmanager.getplugin('html')
            report = outcome.get_result()
            extra = getattr(report, 'extra', [])
            if config.ReportType == "html" or config.ReportType == "both":
                if app:
                    app.save_screenshot(config.screenshot_folder + "failed_desktop" + '.png')
                    extra.append(pytest_html.extras.image(config.screenshot_folder + "failed_desktop" + '.png'))
                    report.extra = extra

        if config.desktop_engine == "pywinauto":
            if config.ReportType == "allure" or "both":
                if app:
                    img = app.capture_as_image().save(config.screenshot_folder + "failed" + '.png')
                    logger.warn(config.screenshot_folder + "failed" + '.png')
                    allure.attach.file(config.screenshot_folder + "failed" + '.png', name='screenshot',
                                       attachment_type=allure.attachment_type.PNG)
                # allure.attach(Image.open(config.screenshot_folder + "failed" + '.png'),
                #               name='screenshot',
                #               attachment_type=allure.attachment_type.PNG)
                pytest_html = item.config.pluginmanager.getplugin('html')
            report = outcome.get_result()
            extra = getattr(report, 'extra', [])
            if config.ReportType == "html" or config.ReportType == "both":
                if app:
                    app.capture_as_image().save(config.screenshot_folder + "failed_desktop" + '.png')
                    extra.append(pytest_html.extras.image(config.screenshot_folder + "failed_desktop" + '.png'))
                    report.extra = extra


# initialize browser in selenium bdd module
def pytest_bdd_before_scenario(request, feature, scenario):
    """Called before scenario is executed."""
    global d, run_config
    browser_value = run_config['browser']
    browser = browser_value.lower()
    url = run_config['bdd_url']
    exec_type = run_config['exec_type']
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


# to call scripting driver in your test function
@pytest.fixture
def driver():
    global d
    before_scenario()
    yield d
    d.quit()


# connection to db fixture
@pytest.fixture
def db_connection():
    global run_config
    db_uri = run_config['db_uri']
    engine = create_engine(db_uri)
    conn = engine.connect()
    yield conn
    conn.close()


# pytest fixture for soap client testing, the function name when called in your test
# will return the yield value as test setup
@pytest.fixture
def soap_client():
    global run_config
    test_url = run_config['wsdl_url']
    client = Client(test_url)
    yield client
    del client


# pytest fixture for rest client testing, the function name when called in your test
# will return the yield value as test setup
@pytest.fixture
def rest_client():
    global run_config
    test_url = run_config['rest_url']
    client = PyRest(test_url)
    yield client
    del client


# pytest fixture for Desktop Testing, the function name when called in your test
# will return the yield value as test setup
app = None
@pytest.fixture
def desktop_app():
    global app
    if config.desktop_engine.lower() == 'pywinauto':
        print("inside pywinauto ")
        path = run_config['desktop_app_path']
        app_title = run_config['desktop_app_title']
        app = Application(backend='uia').start(path).connect(path=path, timeout=10)[app_title]
        if app_title == "Calculator":
            app = Desktop(backend="uia").Calculator
        app.set_focus()
        Timings.Fast()
    elif config.desktop_engine.lower() == 'winappdriver':
        app = webdriver.Remote(
            command_executor=run_config['winapp_driver_url'],
            desired_capabilities=run_config['winapp_driver_cap']
        )
    yield app
    if config.desktop_engine.lower() == "pywinauto":
        app.close()
    else:
        app.close()

mob_conn = None
# pytest fixture for Mobile Testing, the function name when called in your test
@pytest.fixture
def mobile_conn():
    # appium_server = subprocess.Popen(config.appium_command, shell=True)
    # time.sleep(5)
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
    # appium_server.terminate()
    # subprocess.Popen(config.node_close_command, shell=True)

# 
# pytest fixture for initiating the Appium Server for Mobile Testing
# @pytest.fixture(scope="session", autouse=True)
# def server_setup_teardown():
#     appium_server = subprocess.Popen(config.appium_command, shell=True)
#     time.sleep(5)
#     yield
#     appium_server.terminate()
#     subprocess.Popen(config.node_close_command, shell=True)

