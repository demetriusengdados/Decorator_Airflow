from airflow import DAG
from airflow.providers.slack.notifications.slack_notifier import SlackNotifier
from datetime import datetime 

with DAG(
    dag_id='notificação',
    start_date= datetime(2023, 11, 5),
    schedule = None
    on_sucess_callback = SlackNotifier(text="Sucesso"),
    on_failure_callback = SlackNotifier(text="Falha"),
):
    task = BashOperator(
        task_id = "nome_task",
        bash_command = "exit 1",
        on_sucess_callback = SlackNotifier(text = "Task Executada com Sucesso") 
    )