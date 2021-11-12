from PyAuto.PyAutoLogger import get_logger
from object_repository.endpoints.api_users import ApiUsers
import allure

logger = get_logger()  # get the logger, which will add logs to allure reports as well


# steps for rest api testing
# best practice to add @allure.step for more insights in allure reports

@allure.step("validate the user last name from reqres")
def validate_last_name_page2_item_2(rest_client, path, value):
    # used method chaining
    # ApiUsers is the endpoint and rest_client is a session created from PyRest
    ApiUsers(rest_client).get_users_page_2().validate_response_status_code(200). \
        validate_json_path_value(path, value)  # json path helps in parsing the json response


@allure.step("validate the list of user id from reqres")
def validate_list_of_id_page_2(rest_client, path, value):
    # write json will write the response received from the request as a json file
    ApiUsers(rest_client).get_users_page_2().validate_response_status_code(200). \
        validate_json_path_value(path, value).write_json('employee_page2.json')


@allure.step("validate total page reqres")
def validate_total_number_of_page(rest_client, key, value):
    # you can also validate the json based on key value pair
    ApiUsers(rest_client).get_users_page_2().validate_response_status_code(200). \
        validate_response_json_key_value(key, value)


@allure.step("validate if the user is created in system")
def validate_user_creation(rest_client, json_data):
    ApiUsers(rest_client).post_user(json_data).validate_response_status_code(201). \
        validate_response_json_key_value('name', json_data['name'])





