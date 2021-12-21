import mysql.connector
from dotenv import dotenv_values
import pandas as pd


class MySqlDb:
  def __init__(self, host_key, user_key, password_key, db_key):
    config = dotenv_values(".env") 
    self.host = config[host_key]
    self.user = config[user_key]
    self.password = config[password_key]
    self.db = config[db_key]

  def query(self,query_sql,csv=''):
    """queries the db, and will dump a csv to local dir if csv arg is not ''"""
    with mysql.connector.connect(
                                  host=self.host,
                                  user=self.user,
                                  password=self.password,
                                  database=self.db
                                ) as prod_db:
      cursor = prod_db.cursor()
      cursor.execute(query_sql)
      cols = [col[0] for col in cursor.description]
      data = cursor.fetchall()
      data = [dict(zip(cols,datum)) for datum in data]
    if csv != '':
      pd.DataFrame(data).to_csv(csv)
    return data

  def execute(self,query_sql):
    """for DDL queries"""
    try: 
      with mysql.connector.connect(
                                  host=self.host,
                                  user=self.user,
                                  password=self.password,
                                  database=self.db
                                ) as prod_db:
        cursor = prod_db.cursor()
        cursor.execute(query_sql)
        prod_db.commit()
    except Exception as e:
      print(e)

  def get_data_dict(self):
    """gets a data dictionary"""  
    query_text =f"""
    select * from information_schema.columns
    where table_schema = '{self.db}'
    order by table_name, ordinal_position
    """
    data = self.query(query_text)
    return self.query_output_to_schema_tree(data)

  def query_output_to_schema_tree(self, query_output):
    """a function that turns data_dict query output into an algo 
    friendly format"""
    schema_tree = {}
    for row in query_output:
        table = row['TABLE_NAME']
        if table not in schema_tree.keys():
            schema_tree[table]={'fields':[], 'primary_key':''}
        field = {}
        field['name'] = row['COLUMN_NAME']
        field['dtype'] = row['COLUMN_TYPE'] 
        field['not_null'] = row['IS_NULLABLE']=='NO' 
        field['default'] = row['COLUMN_DEFAULT']
        field['extra'] = row['EXTRA']
        schema_tree[table]['fields'].append(field)
        if row['COLUMN_KEY']=='PRI':
            schema_tree[table]['primary_key'] = row['COLUMN_NAME'] 
    return schema_tree

  def get_create_table_sql(self, table_name, fields, primary_key = ''):
    """returns create table text"""
    def create_table_sql_field(name, dtype, not_null=True, extra='', default=''):
      not_null = ' NOT NULL' if not_null else ' NULL'
      default = f' DEFAULT {default}' if default is not None else ''
      extra = f' {extra}' if len(extra)>0 else ''
      return f'\t{name} {dtype}{not_null}{default}{extra},\n'
    create_table_sql = f'DROP TABLE IF EXISTS {table_name};\n'
    create_table_sql += f'CREATE TABLE {table_name} (\n'
    fields = [create_table_sql_field(**field) for field in fields]
    fields = ''.join(fields)
    create_table_sql += fields
    if primary_key!='':
      primary_key = f'\n\tPRIMARY KEY({primary_key})\n'
    create_table_sql += primary_key
    create_table_sql += ');'
    return create_table_sql

  def get_all_create_table_sql(self,out_file=''):
    """get all the create tables sql for this db
    and will optionally write it to a sql file"""
    schema_tree = self.get_data_dict()
    create_table_sql_text = ''
    for table, data in schema_tree.items():
      create_table_sql_text += self.get_create_table_sql(table, 
                                                    data['fields'], 
                                                    data['primary_key'])
      create_table_sql_text += '\n'
    if out_file != '':
      with open(out_file+'.sql', 'w') as create_sql:
        create_sql.write(create_table_sql_text)
    return create_table_sql_text

  def copy_to_db(self, new_db):
    ddl_sql = self.get_all_create_table_sql()
    ddl_sql = ddl_sql.split(';')
    for ddl in ddl_sql[:-1]:
      new_db.execute(ddl)
    
  
  