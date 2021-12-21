import mysql.connector
from dotenv import dotenv_values


class ProdDB:

  def __init__(self):
    self.config = dotenv_values(".env") 

  def query(self,query_sql):
    with mysql.connector.connect(
                                  host=self.config['MYSQL_HOST'],
                                  user=self.config['MYSQL_USER'],
                                  password=self.config['MYSQL_PASSWORD'],
                                  database=self.config['MYSQL_DB']
                                ) as prod_db:
      cursor = prod_db.cursor()
      cursor.execute(query_sql)
      data = cursor.fetchall()
    return data

  def get_data_dict(self):
    query_text =f"""
    select * from information_schema.columns
    where table_schema = '{self.config['MYSQL_DB']}'
    order by table_name
    """
    return self.query(query_text)




