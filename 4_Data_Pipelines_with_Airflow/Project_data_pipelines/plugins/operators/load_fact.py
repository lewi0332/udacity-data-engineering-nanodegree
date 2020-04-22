from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 conn_id="",
                 table="",
                 query="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.table = table
        self.query = query

    def execute(self, context):
        """
        Loads data from Redshift staging table to a destination 'fact' table on the same DB 

        PARAMS:
        conn_id = name (string) of connection id in Airflow. Should be a Redshift or Postgres table.
        table = name (string) of destination table 
        query = SQL query (string) to be executed on the DB. 
        """
        self.log.info('LoadFactOperator Starting')
        redshift = PostgresHook(postgres_conn_id=self.conn_id)
        redshift.run(self.query)
        self.log.info('LoadFactOperator complete')
