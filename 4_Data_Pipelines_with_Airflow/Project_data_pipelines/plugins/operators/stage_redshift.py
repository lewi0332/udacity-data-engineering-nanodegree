from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    template_fields = ("s3_key",)
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 region="",
                 file_type="JSON",
                 delimiter=",",
                 ignore_headers=1,
                 json_path='auto',
                 * args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.region = region
        self.file_type = file_type
        self.delimiter = delimiter
        self.ignore_headers = ignore_headers
        self.json_path = json_path

    def execute(self, context):
        """ 
        Copies JSON or CSV data files stored in AWS S3 and transfer them into
        a single AWS Redshift table.

        PARAMS:
        conn_id = name (string) of Airflow connection id to Redshift DB
        aws_credentials_id = name (string) of Airflow connection details to AWS 
        table = name (string) of destination table on AWS Redshift 
        s3_bucket= name (string) of AWS S3 source
        s3_key = path (string) of sour file. Can be given Airflow macros for
                 dynamic file names. 
                 example : "log_data/{ds}" will substitute task 
                 execution date formated YYYY-MM-DD from Airflow DAG. 
        region = string of AWS region of S3 and Redshift DB. Must be in the same region.
        file_type = file type to look for in S3. JSON or CSV. Default of JSON. 
        delimiter = If CSV file type specified, sets the delimiter character to use when 
                    parseing the source CSV file.
        ignore_headers = integer representing the number of rows to skip in the source
                         CSV file. Default to 1.
        json_path = string of file path for explicit JSON mapping. Must be s3 key formated to map
                    JSON data keys to destination columns in the redshfit staging table. 
                    Default to 'auto', which will map matching keys to table columns, ignore
                    non-matching.
        """
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.conn_id)

        self.log.info("Clearing data from destination Redshift table")
        redshift.run(f"DELETE FROM {self.table}")

        self.log.info("Copying data from S3 to Redshift")
        rendered_key = self.s3_key.format(**context)

        s3_path = "s3://" + self.s3_bucket + rendered_key
        self.log.info(f"Retrieving data from {s3_path}")
        if self.file_type.lower() == 'json':
            redshift.run(f"\
                         COPY {self.table} \
                         FROM '{s3_path}'\
                         ACCESS_KEY_ID '{credentials.access_key}'\
                         SECRET_ACCESS_KEY '{credentials.secret_key}'\
                         REGION '{self.region}'\
                         TIMEFORMAT as 'epochmillisecs'\
                         TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL\
                         FORMAT as JSON '{self.json_path}';")

        elif self.file_type.lower() == 'csv':
            redshift.run(f"\
                         COPY {self.table} \
                         FROM '{s3_path}'\
                         ACCESS_KEY_ID '{credentials.access_key}'\
                         SECRET_ACCESS_KEY '{credentials.secret_key}'\
                         REGION '{self.region}'\
                         TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL\
                         CSV 'auto'\
                         IGNOREHEADER {self.ignore_headers}\
                         DELIMITER '{self.delimiter}';")
        else:
            self.log.info("Unkown file format in S3")
            raise
        self.log.info('StageToRedshiftOperator complete')
