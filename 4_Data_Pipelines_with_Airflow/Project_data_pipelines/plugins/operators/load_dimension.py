from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 conn_id="",
                 query="",
                 table="",
                 truncate="",
                 *args, **kwargs):
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.query = query
        self.table = table
        self.truncate = truncate

    def execute(self, context):
        """
        Loads data from staging tables into dimension tables in AWS redshift.

        PARAMS: 
        conn_id = name (string) of connection id stored in redshift
        query = string of SQL query to be used to INSERT data into dimensional tables
        table = name (string) of destination table 
        truncate = boolean - True = replace data in destination table, 
                             False = append data to destination table
        """
        self.log.info('LoadDimensionOperator starting')
        redshift = PostgresHook(postgres_conn_id=self.conn_id)
        if self.truncate:
            redshift.run(f"TRUNCATE TABLE {self.table}")
        formatted_sql = self.query.format(self.table)
        redshift.run(formatted_sql)
        self.log.info(f"Success: {self.task_id}")
