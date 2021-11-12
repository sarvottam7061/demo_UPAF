from zeep import Client
import pytest
import sys
import datetime
import json

sys.path.append("../../")
from config import TestConfig as config
from PyAuto.PyAutoRest import PyRest
import allure
import pickle
import os

# Get browser value from a pickle file

run_config_file = os.path.abspath('../../resources/run_time_config.pkl')
with open(run_config_file, 'rb') as file:
    # A new file will be created
    run_config = pickle.load(file)


failure_analysis_path = run_config['failure_analysis']
failure_analysis_file = failure_analysis_path + "/failures.json"

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
        if config.ReportType == "allure" or config.ReportType == "both":
            html_button = '''
               <center><a href="failed.html" target="_blank"> <button style="background-color: #B22222; text-align: center; color: White;font-size: 23px;padding: 8px;border: none;margin: 50px;width: 50%;">Report </button></a></center>
               '''
            allure.attach(html_button, "Failure Analysis",
                          allure.attachment_type.HTML)


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
    # you can create a session with authentication here
    # eg:
    # client.auth = ('user', 'pass')
    # client.headers.update({'x-test': 'true'})
    yield client
    del client
