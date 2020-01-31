import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS stagingEvents;"
staging_songs_table_drop = "DROP TABLE IF EXISTS stagingSongs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS userTable;"
song_table_drop = "DROP TABLE IF EXISTS songTable;"
artist_table_drop = "DROP TABLE IF EXISTS artistTable;"
time_table_drop = "DROP TABLE IF EXISTS timeTable;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS stagingEvents (
    event_key            IDENTITY(0,1),
    artist               VARCHAR(25),
    auth                 VARCHAR(25) NOT NULL,
    first_name           VARCHAR(25) NOT NULL,
    gender               VARCHAR(1),
    item_in_session      INTEGER NOT NULL,
    last_name            VARCHAR(25) NOT NULL,
    length               FLOAT,
    level                VARCHAR(10),
    location             VARCHAR(50),
    method               VARCHAR(3),
    page                 VARCHAR(8),
    regestration         FLOAT NOT NULL,
    session_id           INTEGER,
    song                 VARCHAR(35),
    status               INTEGER NOT NULL,
    ts                   TIMESTAMP NOT NULL,
    user_agent           VARCHAR(50),
    user_id              INTEGER NOT NULL,


)
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS stagingSongs (
    song_key             IDENTITY(0,1),
    num_songs            INTEGER, 
    artist_id            VARCHAR(18) NOT NULL, 
    artist_latitude      FLOAT, 
    artist_longitude     FLOAT, 
    artist_location      VARCHAR(25), 
    artist_name          VARCHAR(25), 
    song_id              VARCHAR(18) NOT NULL, 
    title                VARCHAR, 
    duration             FLOAT, 
    year                 INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS userTable
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songTable
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artistTable
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS timeTable
""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
