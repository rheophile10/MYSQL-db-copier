from get_schema_from_prod import MySqlDb

prod_db = MySqlDb('MYSQL_HOST','MYSQL_USER','MYSQL_PASSWORD','MYSQL_DB')
test_db = MySqlDb('T_MYSQL_HOST','T_MYSQL_USER','T_MYSQL_PASSWORD','T_MYSQL_DB')

#will get a data dictionary 
data_dict = test_db.get_data_dict()

#will dump a create_db_sql.sql file in your project directory
text = prod_db.get_all_create_table_sql('create_db_sql')

#copies prod_db schema to test_db
prod_db.copy_to_db(test_db)
