import webbrowser
import argparse
import subprocess
import shutil
import pandas as pd
import pytest
import os
import sys
sys.path.append("../../")
from PyAuto.PyAutoSmartData import SmartData
from utilities.PyAutoRunner import get_pytest_run_command
from config import TestConfig as config
import platform
from PyAuto.PyAutoFailureAnalysis import predict_failure
my_parser = argparse.ArgumentParser()

my_parser.add_argument('-t',
                       '--tags',
                       nargs='*',
                       action='store',
                       help='mention tests with tags to execute')

my_parser.add_argument('-r',
                       '--rerun_flaky_tests',
                       action='store',
                       help='number of times a flaky test to rerun immediately after failure')

my_parser.add_argument('-p',
                       '--parallel',
                       action='store',
                       help='number of times a flaky test to rerun immediately after failure')

my_parser.add_argument('-l',
                       '--last_failed_tests',
                       action='store_true',
                       help='Adding this will run only the tests that are failed during last run')

my_parser.add_argument('-s',
                       '--test_scripts',
                       nargs='*',
                       action='store',
                       help='path to the test file or test folder')

my_parser.add_argument('-b',
                       '--browser',
                       action='store',
                       help='browser to run tests on')

my_parser.add_argument('-m',
                       '--max_fail',
                       action='store',
                       help='maximum number of failure allowed in a test run')

my_parser.add_argument('-j',
                       '--jenkins',
                       action='store_true',
                       help='execution triggered from jenkins')

my_parser.add_argument('-d',
                       '--docker',
                       action='store_true',
                       help='execution triggered from docker')

my_parser.add_argument('-c',
                       '--command_pytest',
                       action='store',
                       help='pass pytest commands through run test, use double quotes for more than one command')

my_parser.add_argument('-u',
                       '--web_url',
                       action='store',
                       help='test url to override the url mentioned in Test config')

args = my_parser.parse_args()

# --------------------------------------------------------------
if config.parallel or args.parallel:
    SmartData().write_smart_data_to_excel()

# ---------------------------------------------------------------

run_command, allure_result_path, allure_report_path, html_report_path, failure_analysis_path = get_pytest_run_command(args,
                                                                                               run_mode_type="scripting",
                                                                                               run_app_type="Web",
                                                                                               script_folder="file_scripts")

if __name__ == '__main__':
    pytest.main(run_command)
    if config.analyze_failures:
        predict_failure(failure_analysis_path)
    if config.ReportType == "html":
        if not args.jenkins and not args.docker:
            webbrowser.open("file:///" + html_report_path + "\\report.html")
    if config.ReportType == "allure":
        if platform.system() == 'Windows':
            subprocess.run(["allure.bat", "generate", "-o", allure_report_path, allure_result_path, "--clean"],
                           shell=False)
            if os.path.isfile(failure_analysis_path + '/failed.html'):
                shutil.copyfile(failure_analysis_path + '/failed.html', allure_report_path+'/data/attachments/failed.html')
        else:
            subprocess.run(["allure", "generate", "-o", allure_report_path, allure_result_path, "--clean"],
                           shell=False)
            if os.path.isfile(failure_analysis_path + '/failed.html'):
                shutil.copyfile(failure_analysis_path + '/failed.html', allure_report_path+'/data/attachments/failed.html')
        if not args.jenkins and not args.docker:
            if platform.system() == 'Windows':
                subprocess.run(["allure.bat", "open", allure_report_path, "-h", "localhost"], shell=False)
            else:
                subprocess.run(["allure", "open", allure_report_path, "-h", "localhost"], shell=False)

    if config.ReportType == "both":
        webbrowser.open("file:///" + html_report_path + "\\report.html")
        if platform.system() == 'Windows':
            subprocess.run(["allure.bat", "generate", "-o", allure_report_path, allure_result_path, "--clean"],
                           shell=False)
            if os.path.isfile(failure_analysis_path + '/failed.html'):
                shutil.copyfile(failure_analysis_path + '/failed.html', allure_report_path+'/data/attachments/failed.html')
        else:
            subprocess.run(["allure", "generate", "-o", allure_report_path, allure_result_path, "--clean"],
                           shell=False)
            if os.path.isfile(failure_analysis_path + '/failed.html'):
                shutil.copyfile(failure_analysis_path + '/failed.html', allure_report_path+'/data/attachments/failed.html')
        if not args.jenkins and not args.docker:
            if platform.system() == 'Windows':
                subprocess.run(["allure.bat", "open", allure_report_path, "-h", "localhost"], shell=False)
            else:
                subprocess.run(["allure", "open", allure_report_path, "-h", "localhost"], shell=False)

# generate_email_report_path = os.path.abspath('../../reports/allurereports/results')
#
# for root, dirs, files in os.walk(generate_email_report_path):
#     for file in files:
#         os.remove(os.path.join(root, file))
#
# for root, dirs, files in os.walk(mydir):
#     for file in files:
#         shutil.copy(os.path.join(root, file), generate_email_report_path)

# get_emailable_report_url = "http://localhost:5050/allure-docker-service/emailable-report/export?project_id=allurereports"
# fileName = mydir+ "\\html-reports\\allure_html_report.html"
#
# response = requests.get(url=get_emailable_report_url)
# chunk_size = 100
# with open(fileName, 'wb') as fd:
#     for chunk in response.iter_content(chunk_size):
#         fd.write(chunk)


# print("file:///"+mydir+"\\html-reports\\report.html")
