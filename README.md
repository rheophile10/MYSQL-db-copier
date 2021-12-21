# MYSQL DB Copier

Gets the schema from a MYSQL DB and will copy it to a new db. Use this to create a test db. 

## TODOs and WARNINGS for the UNWARY

- I need to write tests and schema validation routines. 
- There may be edge cases for create db scripts I haven't seen yet. 
- The MYSQL written here is for MYSQL 5.7 and as such may not be compatible with earlier versions. 

Contributions are welcome.

## Setup

setup a python virtual environment 

```bash
python -m venv virtualenv
virtualenv\\scripts\\activate
pip install -r requirements.txt
```

You also need a .env file in the project directory that has connection details for both dbs

```env
MYSQL_USER="root"
MYSQL_PASSWORD="your_moms_favourite_food"
MYSQL_HOST="127.49.209.72"
MYSQL_DB="your_moms_recipes"

T_MYSQL_USER="root"
T_MYSQL_PASSWORD="my_favourite_food"
T_MYSQL_HOST="127.49.209.73"
T_MYSQL_DB="my_recipes"
```
(you can make up better keys)

## Example Use
Here is how you can use this:

```python
from get_schema_from_prod import MySqlDb

prod_db = MySqlDb('MYSQL_HOST','MYSQL_USER','MYSQL_PASSWORD','MYSQL_DB')
test_db = MySqlDb('T_MYSQL_HOST','T_MYSQL_USER','T_MYSQL_PASSWORD','T_MYSQL_DB')

#will get a data dictionary 
data_dict = test_db.get_data_dict()

#will dump a create_db_sql.sql file in your project directory
text = prod_db.get_all_create_table_sql('create_db_sql')

#copies prod_db schema to test_db
prod_db.copy_to_db(test_db)
```


  
