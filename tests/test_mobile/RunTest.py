import webbrowser
import argparse
import subprocess
import pytest
import sys
sys.path.append("../../")
from utilities.PyAutoRunner import get_pytest_run_command
from config import TestConfig as config
import platform
from PyAuto.PyAutoFailureAnalysis import predict_failure
import shutil
import os

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

my_parser.add_argument('-id',
                       '--mob_udid',
                       action='store',
                       help='UDID number of the mobile device')

my_parser.add_argument('-os',
                       '--mob_platform',
                       action='store',
                       help='OS running in the mobile device')

my_parser.add_argument('-ru',
                       '--mob_remote_url',
                       action='store',
                       help='Remote URL to connect with mobile device')

args = my_parser.parse_args()

run_command, allure_result_path, allure_report_path, html_report_path, failure_analysis_path = get_pytest_run_command(args,
                                                                                               run_mode_type="scripting",
                                                                                               run_app_type="Mobile",
                                                                                               script_folder="file_mobile_auto")

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
            subprocess.run(["allure.bat", "generate", "-o", allure_report_path, allure_result_path, "--clean"], shell=False)
            if os.path.isfile(failure_analysis_path + '/failed.html'):
                shutil.copyfile(failure_analysis_path + '/failed.html', allure_report_path+'/data/attachments/failed.html')
        else:
            subprocess.run(["allure", "generate", "-o", allure_report_path, allure_result_path,"--clean"],
                           shell=False)
            if os.path.isfile(failure_analysis_path + '/failed.html'):
                shutil.copyfile(failure_analysis_path + '/failed.html', allure_report_path+'/data/attachments/failed.html')
        if not args.jenkins and not args.docker:
            if platform.system() == 'Windows':
                subprocess.run(["allure.bat", "open", allure_report_path, "-h", "localhost"], shell=False)
            else:
                subprocess.run(["allure", "open", allure_report_path, "-h", "localhost"], shell=False)