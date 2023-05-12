from datetime import datetime 

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import ShortCircuitOperator
from ariflow.utils.trigger_rule import TriggerRule

with DAG(dag_id="short_dag", start_date = datetime(2023, 12, 5), catchup = False)as dag:
    [task_1, task_2, task_3, task_4, task_5, task_6] = [
        EmptyOperator(task_id=f"task_{i}") for i in range(1, 7)
    ]

    task_7 = EmptyOperator(task_id="task_7", trigger_rule = TriggerRule.ALL_DONE)

    short_circuit = ShortCircuitOperator(
        task_id="short_circuit", python_callable = lambda: False 
    )

    chain(task_1, [task_2, task_3, task_4, task_5, task_6], task_7)

    