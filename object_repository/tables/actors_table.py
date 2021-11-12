from sqlalchemy.sql import text

# have all the queries specific to a table here
# if your query involves multiple table, use common_table.py

# queries can be string
query_first_name_johny = "SELECT * From actor " \
                         "WHERE first_name='JOHNNY'"

# you can use sqlalchemy text function, to pass params to string x and y here
query_name_mathew_johansson = text("SELECT * FROM actor "
                                   "Where first_name=:x AND last_name=:y").bindparams(x='MATTHEW',
                                                                                      y='JOHANSSON')

query_actor_id_196 = text("Select * From actor where actor_id =:n").bindparams(n=196)

query_actor_id_greater_20 = "Select actor_id, first_name, last_name From actor where actor_id>20"
