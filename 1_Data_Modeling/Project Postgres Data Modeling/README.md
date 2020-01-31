# Postgres ETL Project
This is the first project to be delivered for Data Engineering Nanodegree from Udacity. The course module is focused on learning data modeling technics such as normalization/denormalization, learning the star schema, using fact and dimensional tables and the ETL process in python.  

## Motivation
The project works with an imaginary music streaming service called Sparkify. The aim is to build a database for the analytics team of Sparkify to use to find insights into what songs users are listening to
The python scripts in this repository will build a new database and create tables to allow for comprehensive analytics. Therefore we will model our data to be optimaized for an OLAP structure. Allowing for complex analytical and ad hoc queries. Further, we will load data into these tables from an existing store of JSON files stored in a folder heirarchy. 

---

## Data
The data availble to build our database will come from two sources
- Song Data - A json file with data about each song in the Sparkify Library
    - num_songs: `Integer` - Total number of songs in this file
    - artist_id: `String` - a unique id of the artist who performed the song. Id is a mix of alpha and numeric characaters
    - artist_latitude: `Float` -  global coordinates of the artist
    - artist_longitude: `Float` - global coordinates of the artist
    - artist_location: `String` - A loose description of the location of the artist
    - artist_name: `String` - Name of artist
    - song_id: `String` - a unique id of the song file. Id is a mix of alpha and numeric characaters
    - title: `String` - title of the song
    - duration: `Float` - lentgh of the song
    - year: `Integer` - year the song was produced

- Log data - A log of each action taken by users of Sparkify

    - artist: `String` - Name of the artist the user listened to
    - auth: `String` - login status
    - firstName: `String` - firstname of the user 
    - gender: `String` - single character representing the gender of the user
    - itemInSession:  `Integer` - the count and order of plays in this session
    - lastName: `String` - last name of user
    - length: `Float` - how long the user listened to the song
    - level: `String` - subscription status of the user
    - location: `String` - loose description of the location of the user
    - method: `String` - 'GET' or 'PUT'... maybe API call type?  I have no idea. 
    - page: `String` - specific page visited by the user. nextSong an indeicator of songplay
    - registration: `Integer` - No clue what this is.
    - sessionId: `Integer` - Unique count of sessions by the user.
    - song: `String` - Title of song listened to by the user
    - status: `Integer` - HTML status code 
    - ts: `Float` - Timestamp of the start of the songplay
    - userAgent": `String` - type of browser and computer details of the user
    - userId": `String` - A number to represent the user

--- 

## Step 1 Creating tables
For analytical flexibility this project uses a star schema database with a Fact table conected to multiple dimension tables for faster queries. 

**Fact Table**

This table will be built on core facts of actions taken. Therefore, we will focus on making a record of each song play. 
    
    songplay:
        - songplay_id - Primary Key
        - start_time
        - user_id
        - level
        - song_id
        - artist_id
        - session_id
        - location
        - user_agent

**Dimension Tables**

These tables will be related dimensions to be queried for aggregations and detailed analysis.

    users
        - user_id - PRIMARY KEY
        - first_name
        - last_name
        - gender
        - level
    songs
        - song_id PRIMARY KEY
        - title
        - artist_id 
        - year
        - duration
    artists
        - artist_id PRIMARY KEY
        - name
        - location
        - latitude
        - longitude
    time_table
        - start_time
        - hour
        - day
        - week
        - month
        - year
        - weekday

---

## Step 2 Loading Data into the Database
Data is found in multiple directories, transformed from json format and loaded into the database.

- Step 1 - The script connects to our database and creates a cursor object to perform transactions
- Step 2 - Given the filepath to the **main** directory containing the json files, the script will walk over the directory and create a list of every filepath that ends in .json
- Step 3 - Using queries from our sql_queries.py file, the script then uses the .json file to transform the data and insert it into the database.

--- 

## Files 
1. **data** Directory with .json files for both song and log data
2. **sql_queries.py** Python file with SQL queries to drop tables, create tables and insert data.
3. **create_tables.py** Python Script to be run in terminal to delete previous table, and recreate new ones. 
4. **test.ipynb** Jupyter Notbook to test table creation and data insertion.
5. **etl.ipynb** Jupyter Notebook used to build a single insert line to test data transformations.
6. **etl.py** Python Script to read and transform all song_data and log_data and insert them into the database. 
7. **README.md** Markdown file with details on the project.

---
# Execution

1. **Run create_tables.py** - !! Caution - This will remove previous tables and data from teh database !! 
    - In a terminal window change directories to the main directory with both the create_tables.py file.
    - Be certain you have entred the database connection details on line 7: 
        - hostname - dbname - user - password
    - Run the following command in the terminal prompt: 

    `python3 create_tables.py`

2. **Run etl.py** - This will load all data into the newly created tables
    - If you are not in the same terminal window as above, be certain to change directories to the location with both the etl.py script and the data directory.
        - If your data directory is not located in the same folder, you will need to adjust the filepaths on line 113 and 114
    - Run the following command in the terminal prompt: 

    `python3 etl.py`

3. **Test Data**
    - Open the Jupyter Notebook test.ipynb
    - Run these cells in order to connect to the notebook and query the data
    - Check for errors or missing data 
 

## Screenshots
Include logo/demo screenshot etc.

## Tech/framework used


## Features
What makes your project stand out?

## Code Example

Sample process to create tables in the new database

```
songplay_table_create = ("CREATE TABLE IF NOT EXISTS songplay (\
                        songplay_id int PRIMARY KEY,\
                        start_time timestamp,\
                        user_id int NOT NULL,\
                        level varchar,\
                        song_id varchar,\
                        artist_id varchar,\
                        session_id int ,\
                        location varchar,\
                        user_agent varchar)")

user_table_create = ("CREATE TABLE IF NOT EXISTS users (\
                    user_id int PRIMARY KEY,\
                    first_name varchar NOT NULL,\
                    last_name varchar NOT NULL,\
                    gender varchar,\
                    level varchar)")

create_table_queries = [songplay_table_create, user_table_create]

def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
```

Sample function to load data from a json file into the tables.

```
def process_song_file(cur, filepath):
    '''Loads json data from a file and inserts data into the appropriate tables.

        parameters: 
        cur - the SQL connection cursor object to connect to the database
        filepath - a string of the full path to a json file
    '''
    # open song file
    df = pd.read_json(filepath, lines=True)
    print(len(df))
    for i in range(len(df)):
        # insert song record

        song_data = list(
            df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[i])
        cur.execute(song_table_insert, song_data)

        # insert artist record
        artist_data = list(df[['artist_id', 'artist_name', 'artist_location',
                               'artist_longitude', 'artist_latitude']].values[i])
        cur.execute(artist_table_insert, artist_data)
```

## Author 

Derrick Lewis - [Github](https://github.com/lewi0332) - [LinkedIn](https://www.linkedin.com/in/derrick-lewis-551a399/) - [Personal](https://www.derrickjameslewis.com)

## Credits
This project was built from a Udacity Nanodegree template. 

