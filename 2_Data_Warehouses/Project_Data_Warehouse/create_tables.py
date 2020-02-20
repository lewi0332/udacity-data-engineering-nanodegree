import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Deletes and removes any current tables.

    Parameters: 
    cur -- Cursor object for psycopg2
    conn -- connection settings to Postgress for psycopg2
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates tables in AWS Redshift.

    Uses Redshift queries built in sql_queries file and 
    listed in the varibale create_table_queries to create 
    each table.

    Parameters: 
    cur -- Cursor object for psycopg2
    conn -- connection settings to Postgress for psycopg2
    """
    for query in create_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def main():
    """
    Connects to config file for user connection parameters and 
    runs the functions above. 
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
        *config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
