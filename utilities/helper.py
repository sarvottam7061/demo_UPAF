import os
import pickle

from PyAuto.PyAutoLogger import get_logger
from PyAuto.PyAutoReadWrite import ReadWrite
from PyAuto.PyAutoSmartData import SmartData
from config import TestConfig as config

logger = get_logger()


def input_json(**kwargs):
    """
    reads json file and returns json body for a request
    :param kwargs: contains file_name as keyvalue pair
    :return: returns json_body for a request
    """
    json_file_loader = ReadWrite(config.testDataPath, kwargs['file_name'])
    json_body = json_file_loader.load_json()
    return json_body


def verify_token(response, **kwargs):
    """
    verify if the token in present in the response
    :param response: response from rest api call
    :param kwargs: keyward orgs with jwt key
    :return: True or false assert condition
    """
    assert response.json().get(kwargs['jwt_key'])


def save_token(response, **kwargs):
    """
    saves the token fetched from a request
    :param response: response from the request
    :param kwargs: contains file_name to be saved as key value pair
    :return:
    """
    json_file_loader = ReadWrite(config.testDataPath, kwargs['file_name'])
    json_file_loader.write_json(response.json(), kwargs['file_name'])


def convert_to_json(xml_response):
    """
    parses xml_response into json
    :param xml_response:
    :return: return converted json as dictionary
    """
    dict1 = {}
    for i in xml_response:
        dict1[str(i["sName"])] = i["sISOCode"]
    return dict1


def read_json_for_soap(file_name):
    """
    Loads json file for zeep client request
    :param file_name: file_name where we have the json
    :return: return converted json as dictionary
    """
    json_file_loader = ReadWrite(config.testDataPath, file_name)
    json_body = json_file_loader.load_json()
    return json_body


def parametrized_test_data_json_fetch(file_name, test_case_name):
    """
    fetch data from json for parametrized tests
    :param file_name: name of the json file
    :param test_case_name: test case name to be fetched from
    :return: return the json as a list of data
    """

    # --------------------------------------------------------------------------------
    run_config_file = os.path.abspath('../../resources/run_time_config.pkl')
    with open(run_config_file, 'rb') as file:
        run_config = pickle.load(file)
    # --------------------------------------------------------------------------------

    if config.parallel or run_config['parallel']:
        broken_name = file_name.split(".")
        test_data_name = broken_name[0] + "_generated." + broken_name[1]
        json_test_data = ReadWrite(config.testDataPath, test_data_name)
        jtd = json_test_data.load_json()
    else:
        json_test_data = ReadWrite(config.testDataPath, file_name)
        jdf = json_test_data.load_json()
        jtd = SmartData.json_data_sequential(jdf)
        # print(jtd)

    parametrized_test_data_json = json_test_data.get_parametrized_values_json(jtd, test_case_name)
    print(parametrized_test_data_json)
    return parametrized_test_data_json


def parametrized_test_data_excel_fetch(file_name, sheet_name):
    """
    fetch data from excel for parametrized tests
    :param file_name: name of the excel file
    :param sheet_name: sheet name in the excel
    :return: return the excel as list of data
    """
    # --------------------------------------------------------------------------------
    run_config_file = os.path.abspath('../../resources/run_time_config.pkl')
    with open(run_config_file, 'rb') as file:
        run_config = pickle.load(file)
    # --------------------------------------------------------------------------------
    if config.parallel or run_config['parallel']:
        broken_name = file_name.split(".")
        test_data_name = broken_name[0] + "_generated." + broken_name[1]
        excel_test_data = ReadWrite(config.testDataPath, test_data_name)
        etd = excel_test_data.load_excel(sheet_name)
    else:
        excel_test_data = ReadWrite(config.testDataPath, file_name)
        edf = excel_test_data.load_excel(sheet_name)
        etd = SmartData.generate_from_excel(edf)

    parametrized_test_data_excel = excel_test_data.get_parametrized_values_excel(etd)
    # print(parametrized_test_data_excel)
    return parametrized_test_data_excel


# parametrized_test_data_excel_fetch("TestData.xlsx", "TC-01")
# parametrized_test_data_json_fetch("TestData.json", "TC-04")
