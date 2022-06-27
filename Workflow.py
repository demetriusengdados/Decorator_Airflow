from datetime import datetime
from airflow import DAG
from airflow.sensors.date_time import DateTimeSensor
 
with DAG(
   "sync_dag",
   start_date=datetime(2021, 12, 22, 20, 0),
   end_date=datetime(2021, 12, 22, 20, 19),
   schedule_interval="* * * * *",
   catchup=True,
   max_active_runs=32,
   max_active_tasks=32
) as dag:
 
   sync_sensor = DateTimeSensor(
       task_id="sync_task",
       target_time="""{{ macros.datetime.utcnow() + macros.timedelta(minutes=20) }}""",
   )