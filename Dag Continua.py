from airflow.decorators import dag, task 
from datetime import datetime

@dag(start_date=datetime(2023, 12, 5),
     schedule="@continuous",
     max_active_runs=1)
def my_continuous_dag():
    @task
    def start():
        pass
my_continuous_dag()
