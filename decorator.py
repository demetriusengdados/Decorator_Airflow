from airflow.decorators import dag
from astro.sql import transform, append
from astro.sql.table import Table
from astro import dataframe

from datetime import datetime, timedelta
import pandas as pd

SNOWFLAKE_CONN = "snowflake"
SCHEMA = "example_schema"

# Start by selecting data from two source tables in Snowflake
@transform
def combine_data(center_1: Table, center_2: Table):
    return """
    SELECT * FROM {center_1}
    UNION 
    SELECT * FROM {center_2}
    """

# Clean data using SQL
@transform
def clean_data(input_table: Table):
    return '''
    SELECT * 
    FROM {input_table} 
    WHERE TYPE NOT LIKE 'Guinea Pig'
    '''

# Switch to Pandas for pivoting transformation
@dataframe
def aggregate_data(df: pd.DataFrame):
    adoption_reporting_dataframe = df.pivot_table(index='DATE', 
                                                values='NAME', 
                                                columns=['TYPE'], 
                                                aggfunc='count').reset_index()
    return adoption_reporting_dataframe

@dag(start_date=datetime(2021, 1, 1),
    max_active_runs=1,
    schedule_interval='@daily', 
    default_args={
        'email_on_failure': False,
        'retries': 0,
        'retry_delay': timedelta(minutes=5)
    },
    catchup=False
    )
def animal_adoptions_etl():
    # Define task dependencies
    combined_data = combine_data(center_1=Table('ADOPTION_CENTER_1', conn_id=SNOWFLAKE_CONN, schema=SCHEMA),
                                center_2=Table('ADOPTION_CENTER_2', conn_id=SNOWFLAKE_CONN, schema=SCHEMA))

    cleaned_data = clean_data(combined_data)
    aggregated_data = aggregate_data(
        cleaned_data,
        output_table=Table('aggregated_adoptions')
    )
    
    # Append transformed data to reporting table
    append(
        conn_id=SNOWFLAKE_CONN,
        append_table=aggregated_data,
        columns=["DATE", "CAT", "DOG"],
        main_table=Table("adoption_reporting", schema="SANDBOX_KENTEND"),
    )

animal_adoptions_etl_dag = animal_adoptions_etl()