import datetime
import json
import os
import pickle
import subprocess
import time

import allure
import pytest
import sys
from appium import webdriver
from pywinauto.timings import Timings

sys.path.append("../../")
from pywinauto import Application
from config import TestConfig as config
import logging


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


run_config_file = os.path.abspath('../../resources/run_time_config.pkl')
with open(run_config_file, 'rb') as file:
    # A new file will be created
    run_config = pickle.load(file)




# browser_value = run_config['browser_mobile']
failure_analysis_path = run_config['failure_analysis']
failure_analysis_file = failure_analysis_path + "/failures.json"
# to attach screenshot for failed tests
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
                    str(os.environ.get('PYTEST_CURRENT_TEST').split(" (call)")[0]): [
                        call.excinfo._getreprcrash().message, now_time]}
                with open(failure_analysis_file, "w") as file:
                    json.dump(data, file, indent=4)
        if config.ReportType == "allure" or config.ReportType == "both":
            allure.attach(conn.get_screenshot_as_png(),
                          name='screenshot',
                          attachment_type=allure.attachment_type.PNG)
            html_button = '''
                       <center><a href="failed.html" target="_blank"> <button style="background-color: #B22222; text-align: center; color: White;font-size: 23px;padding: 8px;border: none;margin: 50px;width: 50%;">Report </button></a></center>
                       '''
            allure.attach(html_button, "Failure Analysis",
                          allure.attachment_type.HTML)
            pytest_html = item.config.pluginmanager.getplugin('html')
        report = outcome.get_result()
        extra = getattr(report, 'extra', [])
        if config.ReportType == "html" or config.ReportType == "both":
            conn.save_screenshot(config.screenshot_folder + "failed" + '.png')
            extra.append(pytest_html.extras.image(config.screenshot_folder + "failed" + '.png'))
            report.extra = extra


# @pytest.fixture(scope="session", autouse=True)
# def server_setup_teardown():
#     appium_server = subprocess.Popen(config.appium_command, shell=True)
#     time.sleep(5)
#     yield
#     appium_server.terminate()
#     subprocess.Popen(config.node_close_command, shell=True)


@pytest.fixture
def mobile_conn():
    # appium_server = subprocess.Popen(appium_command, shell=True)
    # time.sleep(5)
    global conn
    try:
        conn = webdriver.Remote(config.mob_remote_url, config.desiredCapabilities_mobile)
    except:
        if config.desiredCapabilities_mobile['appPackage']:
            config.desiredCapabilities_mobile['app'] = config.mobile_apk_path
            conn = webdriver.Remote(config.mob_remote_url, config.desiredCapabilities_mobile)
        elif config.desiredCapabilities_mobile['bundleId']:
            config.desiredCapabilities_mobile['app'] = config.mobile_ipa_path
            conn = webdriver.Remote(config.mob_remote_url, config.desiredCapabilities_mobile)
        elif config.desiredCapabilities_mobile['browserName']:
            raise Exception(f"Error in launching the browser {config.desiredCapabilities_mobile['browserName']}.")
    yield conn
    conn.quit()

    # if config.mobile_automation_mode.lower() == 'web':
    #     config.desiredCapabilities_mobile['browserName'] = config.desiredCapabilities_mobile_browserName
    #     conn = webdriver.Remote(config.mob_remote_url, config.desiredCapabilities_mobile)
    #     conn.get(config.mobile_web_url)
    # elif config.mobile_automation_mode.lower() == 'native':
    #     config.desiredCapabilities_mobile['appPackage'] = config.desiredCapabilities_mobile_appPackage
    #     config.desiredCapabilities_mobile['appActivity'] = config.desiredCapabilities_mobile_appActivity
    #     try:
    #         conn = webdriver.Remote(config.mob_remote_url, config.desiredCapabilities_mobile)
    #     except:
    #         config.desiredCapabilities_mobile['app'] = config.desiredCapabilities_mobile_app_install
    #         conn = webdriver.Remote(config.mob_remote_url, config.desiredCapabilities_mobile)
