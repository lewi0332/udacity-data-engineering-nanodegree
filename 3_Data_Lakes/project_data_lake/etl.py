import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import StructType as R, StructField as Fld, DoubleType as Dbl, StringType as Str, IntegerType as Int, DateType as Date, TimestampType

config = configparser.ConfigParser()
config.read('dl.cfg')

KEY = config.get('AWS', 'KEY')
SECRET = config.get('AWS', 'SECRET')


def create_spark_session():
    """
    Get or create a spark session
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Retrevies json files of individual songs from an AWS s3 bucket. Sets Data type and
    separates fields into two tables that are written back to S3

    PARAMETERS:
    - Spark: Spark session object
    - input_data: Path to s3 bucket to retrieve json files
    - output_data: Path to s3 bucket to store transformed parquet files
    """

    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'

    # read song data file
    songSchema = R([
        fld("artist_id", Str()),
        fld("artist_latitude", Dbl()),
        fld("artist_location", Str()),
        fld("artist_longitude", Dbl()),
        fld("artist_name", Str()),
        fld("duration", Dbl()),
        fld("num_songs", Int()),
        fld("song_id", Str()),
        fld("title", Str()),
        fld("year", Int())
    ])
    df = spark.read.json('s3a://udacity-dend/song_data/*/*/*/*.json', schema=songSchema))

    # Rename fields
    fields=[("artist_id", "artist_id"),
              ("artist_latitude", "latitude"),
              ("artist_location", "location"),
              ("artist_longitude", "longitude"),
              ("artist_name", "name"),
              ("duration", "duration"),
              ("num_songs", "num_songs"),
              ("song_id", "song_id"),
              ("title", "title"),
              ("year",  "year")]
    exprs = ["{} as {}".format(field[0], field[1]) for field in fields]
    dfNamed = df.selectExpr(*exprs)

    # extract columns to create songs table
    song_fields = ["title", "artist_id", "year", "duration"]
    songs_table = dfNamed.select(song_fields) \
        .dropDuplicates() \
        .withColumn("song_id", monotonically_increasing_id())

    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy(
        "year", "artist_id").parquet(output_data + 'songs/')

    # extract columns to create artists table
    artists_table = ['artist_id', 'name', 'location', 'lattitude', 'longitude']
    artists_table = dfNamed.select(artists_table).dropDuplicates())

    # write artists table to parquet files
    artists_table.write.parquet(output_data + 'artists/')


def process_log_data(spark, input_data, output_data):
    """
    Retrevies json files of individual logs from an AWS s3 bucket. Renames
    fields, sets data type and builds three tables to be written back to s3

    users table is a table of all unique users
    time table is a table of specific units of time for each time stamp
    songplays table is a fact table with a record of each songplay

    PARAMETERS: 
    - Spark: Spark session object
    - input_data: Path to s3 bucket to retrieve json files
    - output_data: Path to s3 bucket to store transformed parquet files
    """
    # get filepath to log data file
    log_data = 'log_data/*/*/*.json'

    # read log data file
    df = spark.read.json(input_data + log_data, schema=logSchema)

    # filter by actions for song plays
    df = df.filter(df.page='NextSong')

    # rename fields
    fields = [("artist", "artist"),
          ("auth", "auth"),
          ("firstName", "first_name"),
          ("gender", "gender"),
          ("itemInSession", "itemInSession"),
          ("lastName", "last_name"),
          ("length", "length"),
          ("level", "level"),
          ("location", "location"),
          ("method", "method"),
          ("page", "page"),
          ("registration", "registration"),
          ("sessionId", "session_id"),
          ("song", "song"),
          ("status", "status"),
          ("ts", "ts"),
          ("userAgent", "user_agent"),
          ("userId", "user_id")
          ]
    exprs = [ "{} as {}".format(field[0],field[1]) for field in fields]
    df = df.selectExpr(*exprs)

    # extract columns for users table
    user_fields = ['user_id', 'first_name', 'last_name', 'gender', 'level']
    users_table = df.select(user_fields).dropDuplicates()

    # write users table to parquet files
    users_table.write.parquet(output_data + 'users/')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: x/1000, Dbl())
    df = df.withColumn('ts2', get_timestamp('ts'))

    # create datetime column from original timestamp column
    df = df.withColumn('start_time', from_unixtime('ts2').cast(dataType=TimestampType()))

    # extract columns to create time table
    time_table = df.select('start_time')\
                        .dropDuplicates()\
                        .withColumn('hour', hour(col('start_time')))\
                        .withColumn('day', dayofmonth(col('start_time')))\
                        .withColumn('week', weekofyear(col('start_time')))\
                        .withColumn('month', month(col('start_time')))\
                        .withColumn('year', year(col('start_time')))\
                        .withColumn('weekday', date_format(col('start_time'), 'E')

    # write time table to parquet files partitioned by year and month
    time_table.write.parquet(output_data + 'time/')

    # read in song data to use for songplays table
    song_df=spark.read.parquet(output_data + 'songs/*/*/*.parquet')

    songs_logs=df.join(song_df, (df.song == song_df.title))

    songplays = songs_logs.join(time_table,
                                artists_songs_logs.start_time == time_table.start_time)\
                          .drop(songs_logs.year)\
                          .drop(songs_logs.start_time)\
                          .withColumn("songplay_id", monotonically_increasing_id())



    # extract columns from joined song and log datasets to create songplays table
    songplays_table=['songplay_id', 'start_time', 'user_id', 'level', 'song_id',
                      'artist_id', 'session_id', 'location', 'user_agent', 'year', 'month']

    songplays=songplays.select(songplays_table)\
                               .repartition("year", "month")

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy(
        "year", "month").parquet(output_data + 'songplays/')


def main():
    spark=create_spark_session()
    input_data="s3a://udacity-dend/"
    output_data="s3a://udacity-data-engineering1"

    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)
    spark.stop()


if __name__ == "__main__":
    main()
