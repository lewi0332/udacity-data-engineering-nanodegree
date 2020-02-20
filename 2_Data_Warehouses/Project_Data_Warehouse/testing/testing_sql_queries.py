import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('../dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS stagingEvents;"
staging_songs_table_drop = "DROP TABLE IF EXISTS stagingSongs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS userTable;"
song_table_drop = "DROP TABLE IF EXISTS songTable;"
artist_table_drop = "DROP TABLE IF EXISTS artistTable;"
time_table_drop = "DROP TABLE IF EXISTS timeTable;"

# CREATE TABLES

staging_events_table_create = ("""
CREATE TABLE IF NOT EXISTS stagingEvents (
    artist               VARCHAR,
    auth                 VARCHAR,
    firstName            VARCHAR,
    gender               VARCHAR,
    iteminSession        INTEGER,
    lastName             VARCHAR,
    length               FLOAT,
    level                VARCHAR,
    location             VARCHAR,
    method               VARCHAR,
    page                 VARCHAR,
    regestration         FLOAT,
    sessionId            INTEGER,
    song                 VARCHAR,
    status               INTEGER,
    ts                   TIMESTAMP,
    userAgent            VARCHAR,
    userId               INTEGER);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS stagingSongs (
    num_songs            INTEGER, 
    artist_id            VARCHAR, 
    artist_latitude      FLOAT, 
    artist_longitude     FLOAT, 
    artist_location      VARCHAR, 
    artist_name          VARCHAR, 
    song_id              VARCHAR, 
    title                VARCHAR, 
    duration             FLOAT, 
    year                 INTEGER
);
""")

# Dist schema tables

dist_schema_create = ("""CREATE SCHEMA IF NOT EXISTS dist;
SET search_path TO dist;""")

dist_songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay (
    songplay_id          INTEGER         IDENTITY(0,1) PRIMARY KEY,
    start_time           TIMESTAMP       NOT NULL SORTKEY,
    user_id              INTEGER         NOT NULL,
    level                VARCHAR         NOT NULL,
    song_id              VARCHAR         NOT NULL DISTKEY,
    artist_id            VARCHAR         NOT NULL,
    session_id           INTEGER,
    location             VARCHAR,
    user_agent           VARCHAR
);
""")

dist_user_table_create = ("""
CREATE TABLE IF NOT EXISTS userTable (
    user_id              INTEGER          SORTKEY PRIMARY KEY,
    first_name           VARCHAR(255)     NOT NULL,
    last_name            VARCHAR(255)     NOT NULL,
    gender               VARCHAR(1),
    level                VARCHAR(10)
);
""")

dist_song_table_create = ("""
CREATE TABLE IF NOT EXISTS songTable (
    song_id              VARCHAR         SORTKEY PRIMARY KEY,
    title                VARCHAR,
    artist_id            VARCHAR(18)     NOT NULL,
    year                 INTEGER,
    duration             FLOAT
);
""")

dist_artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artistTable (
    artist_id            VARCHAR(18)     SORTKEY PRIMARY KEY,
    name                 VARCHAR,
    location             VARCHAR,
    latitude             FLOAT,
    longitude            FLOAT
);
""")

dist_time_table_create = ("""
CREATE TABLE IF NOT EXISTS timeTable (
    start_time           TIMESTAMP       SORTKEY PRIMARY KEY,
    hour                 INTEGER,
    day                  INTEGER,
    week                 INTEGER,
    month                INTEGER,
    year                 INTEGER,
    weekday              VARCHAR
);
""")

# No dist schema tables

no_dist_schema_create = ("""CREATE SCHEMA IF NOT EXISTS nodist;
SET search_path TO nodist;""")

no_dist_songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay (
    songplay_id          INTEGER         IDENTITY(0,1) PRIMARY KEY,
    start_time           TIMESTAMP       NOT NULL SORTKEY DISTKEY,
    user_id              INTEGER         NOT NULL,
    level                VARCHAR         NOT NULL,
    song_id              VARCHAR         NOT NULL,
    artist_id            VARCHAR         NOT NULL,
    session_id           INTEGER,
    location             VARCHAR,
    user_agent           VARCHAR
);
""")

no_dist_user_table_create = ("""
CREATE TABLE IF NOT EXISTS userTable (
    user_id              INTEGER          NOT NULL SORTKEY PRIMARY KEY,
    first_name           VARCHAR(255)     NOT NULL,
    last_name            VARCHAR(255)     NOT NULL,
    gender               VARCHAR(1),
    level                VARCHAR(10)
);
""")

no_dist_song_table_create = ("""
CREATE TABLE IF NOT EXISTS songTable (
    song_id              VARCHAR         NOT NULL SORTKEY PRIMARY KEY,
    title                VARCHAR         NOT NULL,
    artist_id            VARCHAR(18)     NOT NULL,
    year                 INTEGER         NOT NULL,
    duration             FLOAT
);
""")

no_dist_artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artistTable (
    artist_id            VARCHAR(18)     NOT NULL SORTKEY PRIMARY KEY,
    name                 VARCHAR,
    location             VARCHAR,
    latitude             FLOAT,
    longitude            FLOAT
);
""")

no_dist_time_table_create = ("""
CREATE TABLE IF NOT EXISTS timeTable (
    start_time           TIMESTAMP        NOT NULL SORTKEY DISTKEY PRIMARY KEY,
    hour                 INTEGER          NOT NULL,
    day                  INTEGER          NOT NULL,
    week                 INTEGER          NOT NULL,
    month                INTEGER          NOT NULL,
    year                 INTEGER          NOT NULL,
    weekday              VARCHAR
);
""")

# STAGING TABLES

staging_events_copy = (f"\
    COPY stagingEvents \
    FROM {config['S3']['LOG_DATA']}\
    CREDENTIALS 'aws_iam_role={config['IAM_ROLE']['ARN']}'\
    REGION 'us-west-2' \
    FORMAT as JSON {config['S3']['LOG_JSONPATH']}\
    timeformat as 'epochmillisecs';")

staging_songs_copy = (f"\
    COPY stagingSongs \
    FROM {config['S3']['SONG_DATA']}\
    CREDENTIALS 'aws_iam_role={config['IAM_ROLE']['ARN']}'\
    REGION 'us-west-2' \
    FORMAT as JSON 'auto';")

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT(e.ts)             AS start_time,
           e.userId::INTEGER          AS user_id,
           e.level                    AS level,
           s.song_id                  AS song_id,
           s.artist_id                AS artist_id,
           e.sessionId                AS session_id,
           e.location                 AS location,
           e.userAgent                AS user_agent
    FROM stagingEvents e
    JOIN stagingSongs s ON s.title = e.song AND s.artist_name = e.artist
    WHERE page = 'NextSong' AND user_id IS NOT NULL;""")

user_table_insert = ("""
    INSERT INTO userTable (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT(userId)  AS user_id,
           firstName         AS first_name,
           lastName          AS last_name,
           gender,
           level
    FROM stagingEvents
    WHERE user_id IS NOT NULL 
    AND page = 'NextSong';""")

song_table_insert = ("""
    INSERT INTO songTable (song_id, title, artist_id, year, duration)
    SELECT DISTINCT(song_id) AS song_id,
           title,
           artist_id,
           year,
           duration
    FROM stagingSongs
    WHERE song_id is NOT NULL;""")

artist_table_insert = ("""
    INSERT INTO artistTable (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT(artist_id)  AS artist_id, 
           artist_name          AS name,
           artist_location      AS location,
           artist_latitude     AS latitude,
           artist_longitude     AS longitude
    FROM stagingSongs
    WHERE artist_id IS NOT NULL""")

time_table_insert = ("""
    INSERT INTO timeTable (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT(start_time)                AS start_time,
           EXTRACT(hour FROM start_time)       AS hour,
           EXTRACT(day FROM start_time)        AS day,
           EXTRACT(week FROM start_time)       AS week,
           EXTRACT(month FROM start_time)      AS month,
           EXTRACT(year FROM start_time)       AS year,
           EXTRACT(dayofweek FROM start_time)  as weekday
    FROM songplay;""")

# QUERY LISTS

staging_create_table_queries = [
    staging_events_table_create, staging_songs_table_create]

dist_create_table_queries = [dist_schema_create, staging_events_table_create, staging_songs_table_create,
                             dist_songplay_table_create, dist_user_table_create, dist_song_table_create,
                             dist_artist_table_create, dist_time_table_create]

no_dist_create_table_queries = [no_dist_schema_create, staging_events_table_create, staging_songs_table_create,
                                no_dist_songplay_table_create, no_dist_user_table_create,
                                no_dist_song_table_create, no_dist_artist_table_create,
                                no_dist_time_table_create]

drop_table_queries = [staging_events_table_create, staging_songs_table_create,
                      dist_songplay_table_create, dist_user_table_create, dist_song_table_create,
                      dist_artist_table_create, dist_time_table_create,
                      no_dist_songplay_table_create, no_dist_user_table_create,
                      no_dist_song_table_create, no_dist_artist_table_create,
                      no_dist_time_table_create]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert,
                        song_table_insert, artist_table_insert, time_table_insert]
