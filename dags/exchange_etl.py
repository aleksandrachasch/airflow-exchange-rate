
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks import PostgresHook

from datetime import datetime, timedelta  
import datetime as dt
import requests
import json

###########################################
# DEFINE AIRFLOW DAG (SETTINGS + SCHEDULE)
############################################
default_args = {
     'owner': 'airflow',
     'depends_on_past': False,
     'email': ['user@gmail.com'],
     'email_on_failure': False,
     'email_on_retry': False,
    }

dag = DAG( 'exchangerate_analysis_ETL_3H',
            default_args=default_args,
            description='Collect BTC/USD Exchange Rate',
            catchup=False, 
            start_date= datetime(2022, 5, 31), 
            schedule_interval=timedelta(hours=3)
          )  

####################################################
# DEFINE PYTHON FUNCTIONS
####################################################

def fetch_rate_function(**kwargs):
    print('1 Fetching exchange rate')

    url = 'https://api.exchangerate.host/latest?base=BTC&symbols=USD&source=crypto'
    response = requests.get(url)
    data = response.json()

    return data
    print('Completed \n\n')


def load_data(ti, **kwargs):

    pg_hook  = PostgresHook(postgres_conn_id='postgres_local')

    ds=ti.xcom_pull(key='return_value', task_ids='fetch_rate_task')

    print(ds)

    row  =  ("BTC/USD", ds['date'], ds['rates']['USD'])

    insert_cmd = """INSERT INTO rate (pair, date, rate)
                    VALUES (%s, %s, %s);"""
    pg_hook.run(insert_cmd, parameters=row)



##########################################
# DEFINE AIRFLOW OPERATORS
##########################################

create_table_sql_query = """ 
CREATE TABLE IF NOT EXISTS Rate (pair VARCHAR(250), date VARCHAR(250), rate VARCHAR(250));
"""

create_table = PostgresOperator(
    sql = create_table_sql_query,
    task_id = "create_table_task",
    postgres_conn_id = "postgres_local",
    dag = dag
    )

fetch_rate_task = PythonOperator(task_id = 'fetch_rate_task', 
                                   python_callable = fetch_rate_function, 
                                   provide_context = True,
                                   dag= dag)

insert_into_db_task =  PythonOperator(task_id='load_into_postgres_task',
                                   provide_context=True,
                                   python_callable=load_data,
                                   dag=dag)

create_table >> fetch_rate_task >> insert_into_db_task
