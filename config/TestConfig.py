import platform
import os

# test url
# web_url = "https://demo.seleniumeasy.com/"  # traditional test
web_url = "https://dev103410.service-now.com/navpage.doa"
bdd_url = "https://demo.seleniumeasy.com/"
rest_url = "https://reqres.in/"  # rest api url
wsdl_url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"  # soap test wsdl
# Database engine string for connection
# db_uri = 'postgresql://postgres:455546@localhost:5432/dvdrental'  # for postgres
# db_uri = 'mysql://root:455546@localhost:3306/dvd' #for mysql
db_uri = 'sqlite:///../../resources/movies.db'  # for sqlite

# Browser settings
# values = chrome or edge or firefox or ie or remote
browser = "chrome"
manage_driver = True
# Path to Driver
safari_driver = "/usr/bin/safaridriver"
chrome_driver = "../../drivers/chromedriver.exe"
gecko_driver = "../../drivers/geckodriver.exe"
ie_driver = "../../drivers/iedriver.exe"
edge_driver = "../../drivers/edgedriver.exe"

# options to be added - ci refers to jenkins or docker execution
chromeOptions = {'local': ['--start-maximized', '--disable-extensions'],
                 'ci': ['--disable-extensions', '--headless', '--no-sandbox', '--disable-gpu',
                        '--window-size=1920,1200']}
fireFoxOptions = {'local': ['--disable-extensions'],
                  'ci': ['--headless']}
edgeOptions = {'local': ['--start-maximized'],
               'ci': ['--headless']}
IEOptions = {'local': ['--start-maximized'],
             'ci': ['--headless']}
# chromeOptions = ('disable-extensions', 'start-maximized', 'headless')
# remote execution
remoteOptions = {"url": "http://selenium-hub:4444/wd/hub"}
desiredCapabilities_chrome = {"browserName": "chrome", "browserVersion": 91.0, "platform": "windows"}
desiredCapabilities_firefox = {"browserName": "firefox", "browserVersion": "89.0", "platform": "LINUX"}
desiredCapabilities_remote = desiredCapabilities_firefox


#Windows Desktop Automation settings
desktop_app_path = "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"  # calculator # "calculator.exe"
desktop_app_title = "Calculator"
desktop_engine = "winappdriver"

# desktop_app_path = r"C:/Program Files (x86)/SAP/FrontEnd/SAPgui/saplogon.exe"  # SAP APP
# desktop_app_title = "SAPLogon750"
# desktop_engine = "pywinauto"

winapp_driver_url = "http://127.0.0.1:4723"
winapp_driver_cap = desired_caps = {
    "app": desktop_app_path
}
# winapp_server_path = r'start cmd /c "C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"'


# Mobile Automation Settings

mob_udid = 'ZY2243HFS7'  # UDID specific for every mobile device
mob_platform = 'android'  # Mobile OS
mob_remote_url = 'http://localhost:4723/wd/hub'  # Remote URL for the connection

mobile_ipa_path = ''
mobile_apk_path = 'C:\\Users\\ASUS\\Downloads\\apk_mob\\ECommerce_Demo_v3.apk'
mobile_web_url = "https://www.seleniumeasy.com/test/"

appium_command = "start cmd /c appium"
node_close_command = "start cmd /c taskkill /F /IM node.exe"

# Folder Paths
# Path to test data folder
testDataPath = os.path.abspath("../../testData/") + "/"
# testDataPath = os.path.abspath("E:/automate/PyAutomation_Master_V1/testData/") + "/"
testDataFileName = "TestData.xlsx"
# testDataFileName = "TestData.json"
resourcesFolderPath = os.path.abspath("../../resources/") + "/"
# Screenshot path - has to be set when framework is set up
screenshot_folder = os.path.abspath("../../resources/screenshots/") + "/"
object_repo_path = os.path.abspath("../../resources/object_repo.db")

# wait times
# Explicit wait time to identify locators and poll time
explicit_wait = 5
poll_time = 0.2  # for each 0.5 second, the condition will be checked

# implicit wait during driver initialization
implicit_wait = 3

# Parallel Execution - no of Threads
parallel = False
thread_num = 3

# Flaky test flag
# Rerun Attempts for failed tests - set to 0 ->disabled
rerun_flaky_tests = 0

# Maximum failures in a run
max_fail = 100

# last run Failed tests rerun
last_failed_tests = False

# Reporting value - allure or html or both
ReportType = "allure"
ReportType_api = "allure"
ReportType_bdd = "allure"

# Shows the trends and history of runs for all test cases.
# Must be used only for fixed set of test cases that will be run after each release
Allure_History = False

# tags are marked over tests with @pytest.mark.<tag_name>
tags = ["web_healing_test"]
# tags = ["se_input_form"]
# -------------------------------------------------------
# it can be set as empty list, to include all the files in subfolder of where RunTest is present

test_file_e2e = ['e2e_scripts/test_e2e.py', 'e2e_scripts/test_e2e_desktop.py']
# test_file_e2e = ['e2e_step_defs/test_step_def.py']
test_file_scripts = ["selenium_easy_tests/test_selenium_easy.py", "service_now_tests/test_service_now.py"]
test_file_bdd = ["auto_insurance_test/test_selenium_easy.py"]
test_file_api = ["soap_tests/test_soap_request.py", "rest_tests/test_rest_request.py"]
test_file_db = ["dvdrental_tests/test_actors_payment.py"]
test_file_mobile = ["mobile_tests/test_mobile.py"]
test_file_desktop = ["sap_windows_test/test_sap_windows.py"]

# set folder to empty to execute all tests in current and sub folders
# test_file_scripts = []

#run mode can be 'capture', 'heal', 'normal', 'capture&heal'
run_mode = 'capture&heal'
# run_mode = 'normal'
healing_score = 0.5
use_last_healed = False

#Failure Analysis
analyze_failures = True

