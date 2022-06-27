from datetime import datetime
from airflow import DAG
from airflow.sensors.date_time import DateTimeSensorAsync
 
with DAG(
   "async_dag",
   start_date=datetime(2021, 12, 22, 20, 0),
   end_date=datetime(2021, 12, 22, 20, 19),
   schedule_interval="* * * * *",
   catchup=True,
   max_active_runs=32,
   max_active_tasks=32
) as dag:
 
   async_sensor = DateTimeSensorAsync(
       task_id="async_task",
       target_time="""{{ macros.datetime.utcnow() + macros.timedelta(minutes=20) }}""",
   )