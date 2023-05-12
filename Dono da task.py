from airflow import DAG 
from airflow.decorators import task 
from datetime import datetime

DEFAULT_ARGS = {
    "owner": "nome_do_dono_da_task"
}

with DAG(
    dag_id = "my_dag",
    start_date = datetime(2023, 12, 5),
    schedule = "@dailly",
    owner_links = {"dono_da_task": "mailto:seuemail@nomeempresa.com"},
    default_args = DEFAULT_ARGS
):
    @task
    def my_task():
        print("Salva com Sucesso")
    
    my_task()
    