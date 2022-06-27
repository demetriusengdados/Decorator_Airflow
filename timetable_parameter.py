from uneven_intervals_timetable import UnevenIntervalsTimetable

with DAG(
    dag_id="example_timetable_dag",
    start_date=datetime(2021, 10, 9), 
    max_active_runs=1,
    timetable=UnevenIntervalsTimetable(),
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=3),
    },
    catchup=True
) as dag: