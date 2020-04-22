from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 conn_id="",
                 tables=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.tables = tables

    def execute(self, context):
        """
        Checks data quality of explicit tables on the connected DB.
        1. Tests for table names in the database
        2. Tests that included tables have rows
        3. Tests the final column in each table for Null values 

        Params: 
          conn_id : Name of airflow connection id to a Redshift or Postgres DB
          tables : List of table names to test. 
        """
        self.log.info(f'DataQualityOperator Starting with {self.conn_id}')

        redshift = PostgresHook(postgres_conn_id=self.conn_id)
        self.log.info(f'tables:  {self.tables}.')
        self.log.info(f'type(tables):  {type(self.tables)} .')
        for table in self.tables:
            self.log.info(f'--DataQualityOperator checking {table}.')
            records = redshift.get_records(
                sql=f"SELECT COUNT(*) FROM {table};")
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(
                    f"----Data quality check failed. {table} returned no results")
            num_records = records[0][0]
            if num_records < 1:
                raise ValueError(
                    f"----Data quality check failed. {table} contained 0 rows")
        for table in self.tables:
            self.log.info(f'--DataQualityOperator checking {table}.')
            records = redshift.get_records(
                sql=f"SELECT COUNT(*) - COUNT(-1) FROM {table};")
            self.log.info(f'records[0][0] looks like this:  {records[0][0]} .')
            if records[0][0] > 0:
                raise ValueError(
                    f"----Data quality check failed. {table} Last column has Null Values")

        self.log.info(f'----DataQualityOperator {self.conn_id} passed.')
