import allure
from object_repository.tables.actors_table import *
from PyAuto.PyAutoDatabase import PySQLDatabase
from sqlalchemy.sql import text
from PyAuto.PyAutoReadWrite import ReadWrite
from config import TestConfig as config

# database test steps for actor table
@allure.step("check record exists with first name johny")
def check_record_exists_first_name(connection):
    # PySQLDatabase takes connection from sqlalchemy engine
    # This also supports method chaining
    PySQLDatabase(connection).execute_query(query_first_name_johny).check_if_exists()
    
    
@allure.step("check record does not exists with full name")
def check_record_does_not_exists_first_name(connection):
    # PySQLDatabase takes connection from sqlalchemy engine
    # This also supports method chaining
    excel_test_data = ReadWrite(config.testDataPath, "names_new.xlsx")
    edf = excel_test_data.load_excel("name")
    query_excel_names = text("SELECT * FROM actor "
                             "Where first_name=:x AND last_name=:y").bindparams(x=edf['First Name'][0],
                                                                                y=edf['Last Name'][0])
    PySQLDatabase(connection).execute_query(query_name_mathew_johansson).row_count_is_zero()


@allure.step("check record exists with full name mathew johansson")
def check_record_exists_full_name(connection):
    # can use reusable functions present in PySQLDatabase,
    # row count equal to compares the record with query results
    PySQLDatabase(connection).execute_query(query_name_mathew_johansson). \
        row_count_equal_to(1)


@allure.step("Get and validate the row count where id is equal to 196")
def validate_row_count_id(connection):
    # get row count returns the number of records retrieved after the query
    rows = PySQLDatabase(connection).execute_query(query_actor_id_196). \
        get_row_count()
    assert rows == 1


@allure.step("Example to create pandas dataframe from a query")
def get_query_result_as_a_dataframe(connection):
    # you can also use pandas dataframe to retrieve query results and do validation
    df = PySQLDatabase(connection).query_save_data_frame(query_actor_id_greater_20).recordset_df
    # get the pandas dataframe and do all validation, to get row count df.shape[0]
    assert df.shape[0] == 180, f"The total number of rows is not equal to 180"
    # filter operation in dataframe -> equivalent to running a query with condition
    assert df[df['actor_id'] > 40].shape[0] == 160, f"The total number of rows after filtering is not equal to 160"


@allure.step("Example to create pandas dataframe from a table")
def get_table_result_as_a_dataframe(connection):
    # care should be taken to not load sql table with more than 100000 rows or 1 Gb of data as dataframe loads in RAM
    df = PySQLDatabase(connection).table_save_data_frame("actor").recordset_df
    # get the pandas dataframe and do all validation, to get row count df.shape[0]
    assert df.shape[0] == 200, f"The total number of rows is not equal to 200"
    # filter operation in dataframe -> equivalent to running a query with condition
    assert df[df['actor_id'] > 40].shape[0] == 160, f"The total number of rows after filtering is not equal to 160"
