import pytest
from business_components.database_components.actor_table_components import *


@pytest.mark.db_tests
def test_validate_actors_table(db_connection):
    check_record_exists_first_name(db_connection)
    check_record_exists_full_name(db_connection)
    validate_row_count_id(db_connection)


@pytest.mark.db_tests
def test_validate_actors_data_frame(db_connection):
    get_query_result_as_a_dataframe(db_connection)
    get_table_result_as_a_dataframe(db_connection)
