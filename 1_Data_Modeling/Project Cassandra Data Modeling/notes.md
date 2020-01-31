# Notes on NoSql Databases

**When Not to Use SQL:**
- Need high Availability in the data: Indicates the system is always up and there is no downtime
- Have Large Amounts of Data
- Need Linear Scalability: The need to add more nodes to the system so performance will increase linearly
- Low Latency: Shorter delay before the data is transferred once the instruction for the transfer has been received.
- Need fast reads and write

### CAP Theorem:
- Consistency: Every read from the database gets the latest (and correct) piece of data or an error
- Availability: Every request is received and a response is given -- without a guarantee that the data is the latest update
- Partition Tolerance: The system continues to work regardless of losing network connectivity between nodes


### Commonly Asked Questions:
**Is Eventual Consistency the opposite of what is promised by SQL database per the ACID principle?**
Much has been written about how Consistency is interpreted in the ACID principle and the CAP theorem. Consistency in the ACID principle refers to the requirement that only transactions that abide by constraints and database rules are written into the database, otherwise the database keeps previous state. In other words, the data should be correct across all rows and tables. However, consistency in the CAP theorem refers to every read from the database getting the latest piece of data or an error.
To learn more, you may find this discussion useful: https://www.voltdb.com/blog/2015/10/22/disambiguating-acid-cap/

**Discussion about ACID vs. CAP**
Which of these combinations is desirable for a production system - Consistency and Availability, Consistency and Partition Tolerance, or Availability and Partition Tolerance?
As the CAP Theorem Wikipedia entry says, "The CAP theorem implies that in the presence of a network partition, one has to choose between consistency and availability." So there is no such thing as Consistency and Availability in a distributed database since it must always tolerate network issues. You can only have Consistency and Partition Tolerance (CP) or Availability and Partition Tolerance (AP). Remember, relational and non-relational databases do different things, and that's why most companies have both types of database systems.

**Does Cassandra meet just Availability and Partition Tolerance in the CAP theorem?**
According to the CAP theorem, a database can actually only guarantee two out of the three in CAP. So supporting Availability and Partition Tolerance makes sense, since Availability and Partition Tolerance are the biggest requirements.

**If Apache Cassandra is not built for consistency, won't the analytics pipeline break?**
If I am trying to do analysis, such as determining a trend over time, e.g., how many friends does John have on Twitter, and if you have one less person counted because of "eventual consistency" (the data may not be up-to-date in all locations), that's OK. In theory, that can be an issue but only if you are not constantly updating. If the pipeline pulls data from one node and it has not been updated, then you won't get it. Remember, in Apache Cassandra it is about Eventual Consistency.


# THINK ABOUT THE QUERIES FIRST 
There are no joins in Apache Cassandra

Data Modeling in Apache Cassandra:
- Denormalization is not just okay -- it's a must
- Denormalization must be done for fast reads
- Apache Cassandra has been optimized for fast writes
- ALWAYS think Queries first
- One table per query is a great strategy
- Apache Cassandra does not allow for JOINs between tables

Commonly Asked Questions:

**I see certain downsides of this approach, since in a production application, requirements change quickly and I may need to improve my queries later. Isn't that a downside of Apache Cassandra?**
In Apache Cassandra, you want to model your data to your queries, and if your business need calls for quickly changing requirements, you need to create a new table to process the data. That is a requirement of Apache Cassandra. If your business needs calls for ad-hoc queries, these are not a strength of Apache Cassandra. However keep in mind that it is easy to create a new table that will fit your new query.

Additional Resource:
Here is a reference to the DataStax documents on [Apache Cassandra].(https://docs.datastax.com/en/dse/6.7/cql/cql/ddl/dataModelingApproach.html)    

## Primary Key
- Must be unique
- The PRIMARY KEY is made up of either just the PARTITION KEY or may also include additional CLUSTERING COLUMNS
- A Simple PRIMARY KEY is just one column that is also the PARTITION KEY. A Composite PRIMARY KEY is made up of more than one column and will assist in creating a unique value and in your retrieval queries
- The PARTITION KEY will determine the distribution of data across the system   


## Clustering Columns:
- The clustering column will sort the data in sorted ascending order, e.g., alphabetical order. Note: this is a mistake in the video, which says descending order.
- More than one clustering column can be added (or none!)
- From there the clustering columns will sort in order of how they were added to the primary key

### Commonly Asked Questions:
**How many clustering columns can we add?**

You can use as many clustering columns as you would like. You cannot use the clustering columns out of order in the SELECT statement. You may choose to omit using a clustering column in your SELECT statement. That's OK. Just remember to use them in order when you are using the SELECT statement.

## Primary Key in CQL

- A primary key uniquely identifies a row.
- A composite key is a key formed from multiple columns.
- A partition key is the primary lookup to find a set of rows, i.e. a partition.
- A clustering key is the part of the primary key that isn't the partition key (and defines the ordering within a partition).

Examples:

    PRIMARY KEY (a): The partition key is a.
    PRIMARY KEY (a, b): The partition key is a, the clustering key is b.
    PRIMARY KEY ((a, b)): The composite partition key is (a, b).
    PRIMARY KEY (a, b, c): The partition key is a, the composite clustering key is (b, c).
    PRIMARY KEY ((a, b), c): The composite partition key is (a, b), the clustering key is c.
    PRIMARY KEY ((a, b), c, d): The composite partition key is (a, b), the composite clustering key is (c, d).