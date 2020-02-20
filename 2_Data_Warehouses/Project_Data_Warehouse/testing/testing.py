import configparser
from time import time
import psycopg2
import pandas as pd
from testing_sql_queries import *
import plotly.graph_objects as go
import fohr_theme
import plotly


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_dist_tables(cur, conn):
    for query in dist_create_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def create_no_dist_tables(cur, conn):
    for query in no_dist_create_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


config = configparser.ConfigParser()
config.read('../dwh.cfg')

conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
    *config['CLUSTER'].values()))
cur = conn.cursor()

drop_tables(cur, conn)
create_no_dist_tables(cur, conn)
create_dist_tables(cur, conn)

conn.close()


def loadTables(schema):
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
        *config['CLUSTER'].values()))
    cur = conn.cursor()
    loadTimes = []
    cur.execute("SET search_path TO {};".format(schema))
    for query in copy_table_queries:
        cur.execute("set enable_result_cache_for_session to off;" + query)
        conn.commit()

    for table in insert_table_queries:
        print(
            "======= LOADING TABLE: ** {} ** IN SCHEMA ==> {} =======".format(table, schema))
        t0 = time()
        cur.execute("set enable_result_cache_for_session to off;" + table)
        loadTime = time()-t0
        loadTimes.append(loadTime)
        conn.commit()

        print("=== DONE IN: {0:.2f} sec\n".format(loadTime))
    conn.close()
    table_names = ["songplay_table", "user_table",
                   "song_table", "artist_table", "time_table"]
    return pd.DataFrame({"table": table_names, "loadtime_"+schema: loadTimes}).set_index('table')

    # -- List of the tables to be loaded


# -- Insertion twice for each schema (WARNING!! EACH CAN TAKE MORE THAN 10 MINUTES!!!)
distStats = loadTables("dist")
nodistStats = loadTables("nodist")

# -- Plotting of the timing results

stats = distStats.join(nodistStats)
fig = go.Figure()
fig.add_trace(go.Bar(x=stats.index,
                     y=stats['loadtime_dist'], name='Distributed by Song Key'))
fig.add_trace(
    go.Bar(x=stats.index, y=stats['loadtime_nodist'], name='Distributed by Time'))
fig.update_layout(barmode='group', title='AWS Redshift Load Time Comparison')
fig.update_yaxes(title='Seconds')
fig.update_xaxes(title='Tables')
plotly.offline.plot(
    fig, filename='Table load times test 2.html', auto_open=False)

oneDim_SQL = """
set enable_result_cache_for_session to off;
SET search_path TO {};

SELECT sp.user_id, u.first_name, u.last_name, sum(st.duration) as total_time
FROM songplay sp
JOIN userTable u ON sp.user_id = u.user_id
JOIN songTable st ON sp.song_id = st.song_id
JOIN timeTable t ON sp.start_time = t.start_time
WHERE t.weekday = 5 OR t.weekday = 6
GROUP BY 1, 2, 3
ORDER by 4;
"""
#

twoDim_SQL = """
set enable_result_cache_for_session to off;
SET search_path TO {};

SELECT sp.artist_id, a.name, sum(st.duration)
FROM songplay sp
JOIN songTable st ON sp.song_id = st.song_id
JOIN artistTable a ON sp.artist_id = a.artist_id
WHERE sp.level = 'free'
GROUP BY 1, 2
ORDER BY 3 DESC
"""

drill_SQL = """
set enable_result_cache_for_session to off;
SET search_path TO {};

SELECT sp.artist_id, a.name, AVG(t.hour) as Avg_Start_Hour, sum(st.duration) as Total_listen_time
FROM songplay sp
JOIN songTable st ON sp.song_id = st.song_id
JOIN artistTable a ON sp.artist_id = a.artist_id
JOIN timeTable t ON sp.start_time = t.start_time
WHERE sp.level = 'free'
AND st.year < 2017
AND t.month IN (11)
GROUP BY 1, 2
ORDER BY 4 DESC;
"""


oneDimSameDist_SQL = """
set enable_result_cache_for_session to off;
SET search_path TO {};

SELECT sp.start_time, u.level, sp.location
FROM songplay sp
JOIN userTable u ON sp.user_id = u.user_id
WHERE sp.location IS NOT NULL
order by 1
"""


def compareQueryTimes(schema):
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
        *config['CLUSTER'].values()))
    cur = conn.cursor()
    queryTimes = []
    for i, query in enumerate([oneDim_SQL, twoDim_SQL, drill_SQL, oneDimSameDist_SQL]):
        t0 = time()
        q = query.format(schema)
        cur.execute(q)
        queryTime = time()-t0
        queryTimes.append(queryTime)
        conn.commit()
    conn.close()
    return pd.DataFrame({"query": ["oneDim", "twoDim", "drill", "oneDimSameDist"], "queryTime_"+schema: queryTimes}).set_index('query')


distQueryTimes = compareQueryTimes("dist")
noDistQueryTimes = compareQueryTimes("nodist")


queryTimeDF = distQueryTimes.join(noDistQueryTimes)
fig = go.Figure()
fig.add_trace(go.Bar(x=queryTimeDF.index,
                     y=queryTimeDF['queryTime_dist'], name='Distributed by Song ID'))
fig.add_trace(
    go.Bar(x=queryTimeDF.index, y=queryTimeDF['queryTime_nodist'], name='Distributed by Time'))
fig.update_layout(barmode='group', title='AWS Redshift Query Time Comparison')
fig.update_yaxes(title='Seconds')
fig.update_xaxes(title='Queries')
# fig.show()
plotly.offline.plot(fig, filename='Query_times_test 2.html', auto_open=False)

improvementDF = queryTimeDF["distImprovement"] = 100.0*(
    queryTimeDF['queryTime_nodist']-queryTimeDF['queryTime_dist'])/queryTimeDF['queryTime_nodist']
fig = go.Figure()
fig.add_trace(go.Bar(x=improvementDF.index, y=improvementDF))
fig.update_layout(title='Query Time Delta')
fig.update_yaxes(title='Percentage')
fig.update_xaxes(title='Queries')
# fig.show()
plotly.offline.plot(
    fig, filename='Query_time_delta_test 2.html', auto_open=False)


# conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
#     *config['CLUSTER'].values()))
# cur = conn.cursor()
# cur.execute(test.format('dist'))
# rows = cur.fetchall()
# conn.commit()


# test = """
# set enable_result_cache_for_session to off;
# SET search_path TO {};

# SELECT count(*)
# FROM timeTable
# """
# JOIN songTable st ON sp.song_id = st.song_id
# JOIN artistTable a ON sp.artist_id = a.artist_id
# JOIN userTable u ON sp.user_id = u.user_id
# """

# songplay = 1998
# songtable = 89376
# artistTable = 60150
# userTable = 624


def printquerySample(query, schema):
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
        *config['CLUSTER'].values()))
    cur = conn.cursor()
    q = query.format(schema)
    cur.execute(q)
    colnames = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return pd.DataFrame(rows, columns=colnames).head().to_markdown())

for i in [oneDim_SQL, twoDim_SQL, drill_SQL, oneDimSameDist_SQL]:
    print("\n\n", i, "\n")
    print(printquerySample(i, 'dist'))
