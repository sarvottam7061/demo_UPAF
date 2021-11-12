import datetime
import json
import logging
import os
import pickle
import subprocess
import threading
import time

from PyAuto.PyAutoSap import PyAutoSap
import allure
import pytest
import sys

from PIL import Image
from pywinauto.timings import Timings
from PyAuto.PyAutoLogger import get_logger

sys.path.append("../../")
from pywinauto import Application, Desktop
from config import TestConfig as config
from appium import webdriver

run_config_file = os.path.abspath('../../resources/run_time_config.pkl')
with open(run_config_file, 'rb') as file:
    # A new file will be created
    run_config = pickle.load(file)

app = None
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

failure_analysis_path = run_config['failure_analysis']
failure_analysis_file = failure_analysis_path + "/failures.json"
# to attach screenshot for failed tests
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    global app
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
        if config.desktop_engine == "winappdriver":
            if config.ReportType == "allure" or "both":
                html_button = '''
                                          <center><a href="failed.html" target="_blank"> <button style="background-color: #B22222; text-align: center; color: White;font-size: 23px;padding: 8px;border: none;margin: 50px;width: 50%;">Report </button></a></center>
                                          '''
                allure.attach(html_button, "Failure Analysis",
                              allure.attachment_type.HTML)
                allure.attach(app.get_screenshot_as_png(),
                              name='screenshot',
                              attachment_type=allure.attachment_type.PNG)
                pytest_html = item.config.pluginmanager.getplugin('html')
            report = outcome.get_result()
            extra = getattr(report, 'extra', [])
            if config.ReportType == "html" or config.ReportType == "both":
                app.save_screenshot(config.screenshot_folder + "failed" + '.png')
                extra.append(pytest_html.extras.image(config.screenshot_folder + "failed" + '.png'))
                report.extra = extra

        if config.desktop_engine == "pywinauto":
            if config.ReportType == "allure" or "both":
                html_button = '''
                  <center><a href="failed.html" target="_blank"> <button style="background-color: #B22222; text-align: center; color: White;font-size: 23px;padding: 8px;border: none;margin: 50px;width: 50%;">Report </button></a></center>
                  '''
                allure.attach(html_button, "Failure Analysis",
                              allure.attachment_type.HTML)
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
                app.capture_as_image().save(config.screenshot_folder + "failed" + '.png')
                extra.append(pytest_html.extras.image(config.screenshot_folder + "failed" + '.png'))
                report.extra = extra


# to call scripting driver in your test function
@pytest.fixture
def desktop_app():
    global app
    if config.desktop_engine.lower() == 'pywinauto':
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
        app.close_app()


@pytest.fixture
def session(desktop_app):
    sap_session = PyAutoSap()
    sap_session.connect_to_session()
    yield sap_session

# @pytest.fixture(autouse=True, scope="session")
# def server_setup_teardown():
#     if config.desktop_engine == "winappdriver":
#         winapp_server = subprocess.Popen(config.winapp_server_path, shell=True)
#         time.sleep(2)
#         yield
#         # winapp_server.communicate(input='\n')
#         subprocess.Popen(r'taskkill /im "C:\windows\system32\cmd.exe" /t /f', shell=True)
#         # C:\windows\system32\cmd.exe
