import pytest
from business_components.api_components.reqres_components import *

logger = get_logger()



@pytest.mark.get_request
def test_user_list(rest_client):
    validate_total_number_of_page(rest_client, 'total_pages', 2)
    validate_last_name_page2_item_2(rest_client, '$.data[1].last_name', ['Ferguson'])
    validate_list_of_id_page_2(rest_client, '$.data[*].id', [7, 8, 9, 10, 11, 12])



@pytest.mark.post_request
def test_create_user(rest_client, json_data):
    # if you have single data parametrization(only json_data), we will get a tuple and it has to be converted by indexing
    # or using object destruction *json_data
    # if len(json_data)==1:
    #     json_data= json_data[0]
    validate_user_creation(rest_client, *json_data)


