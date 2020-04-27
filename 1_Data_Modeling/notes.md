
# Data Modeling 
---

## POSTGRES

Codd's 12 rules: https://en.wikipedia.org/wiki/Codd%27s_12_rules


**Normalization** is about trying to increase data integrity by reducing the number of copies of the data. Data that needs to be added or updated will be done in as few places as possible.

**Denormalization** is trying to increase performance by reducing the number of joins between tables (as joins can be slow). Data integrity will take a bit of a potential hit, as there will be more copies of the data (to reduce JOINS).

**Objectives of Normal Form:**
- To free the database from unwanted insertions, updates, & deletion dependencies
- To reduce the need for refactoring the database as new types of data are introduced
- To make the relational model more informative to users
- To make the database neutral to the query statistics


**How to reach First Normal Form (1NF):**

- Atomic values: each cell contains unique and single values
- Be able to add data without altering tables
- Separate different relations into different tables
- Keep relationships between tables together with foreign keys

**Second Normal Form (2NF):**

- Have reached 1NF
- All columns in the table must rely on the Primary Key

**Third Normal Form (3NF):**

- Must be in 2nd Normal Form
- No transitive dependencies
- Remember, transitive dependencies you are trying to maintain is that to get from A-> C, you want to avoid going through B.

**When to use 3NF:**
When you want to update data, we want to be able to do in just 1 place. We want to avoid updating the table in the Customers Detail table (in the example in the lecture slide).

---

### Data Definition and Constraints
The `CREATE` statement in SQL has a few important constraints that are highlighted below.

**NOT NULL**
The **NOT NULL** constraint indicates that the column cannot contain a null value.

Here is the syntax for adding a NOT NULL constraint to the CREATE statement:

```
CREATE TABLE IF NOT EXISTS customer_transactions (
    customer_id int NOT NULL, 
    store_id int, 
    spent numeric
);
```

You can add **NOT NULL** constraints to more than one column. Usually this occurs when you have a **COMPOSITE KEY**, which will be discussed further below.

Here is the syntax for it:
```
CREATE TABLE IF NOT EXISTS customer_transactions (
    customer_id int NOT NULL, 
    store_id int NOT NULL, 
    spent numeric
);
```

**UNIQUE**
The **UNIQUE** constraint is used to specify that the data across all the rows in one column are unique within the table. The **UNIQUE** constraint can also be used for multiple columns, so that the combination of the values across those columns will be unique within the table. In this latter case, the values within 1 column do not need to be unique.

Let's look at an example.
```
CREATE TABLE IF NOT EXISTS customer_transactions (
    customer_id int NOT NULL UNIQUE, 
    store_id int NOT NULL UNIQUE, 
    spent numeric 
);
```
Another way to write a **UNIQUE** constraint is to add a table constraint using commas to separate the columns.
```
CREATE TABLE IF NOT EXISTS customer_transactions (
    customer_id int NOT NULL, 
    store_id int NOT NULL, 
    spent numeric,
    UNIQUE (customer_id, store_id, spent)
);
```
**PRIMARY KEY**
The **PRIMARY KEY** constraint is defined on a single column, and every table should contain a primary key. The values in this column uniquely identify the rows in the table. If a group of columns are defined as a primary key, they are called a **composite key**. That means the combination of values in these columns will uniquely identify the rows in the table. By default, the **PRIMARY KEY** constraint has the unique and not null constraint built into it.

Let's look at the following example:
```
CREATE TABLE IF NOT EXISTS store (
    store_id int PRIMARY KEY, 
    store_location_city text,
    store_location_state text
);
```

Here is an example for a group of columns serving as composite key.

```
CREATE TABLE IF NOT EXISTS customer_transactions (
    customer_id int, 
    store_id int, 
    spent numeric,
    PRIMARY KEY (customer_id, store_id)
);
```

### Fact and Dimension Tables

**Fact Tables**
- Fact table consists of the measurements metrics or facts of a business process. 

**Dimensional Tables**
- A structure that categorizes facts and measures in order to enable users to anser business questions. Dimensions are people products place and time. 

**Star Schema**
- Star Schema is the simplist stule of data mart schema The star schema consist of one or more fact tables reference any number of dimension tables. 

**Snowflake Schema**
- Logical arrangement of tables in a multidimensional database represented by a centralized fact tables which are connected to multiple dimensions. 


### Upsert
In RDBMS language, the term upsert refers to the idea of inserting a new row in an existing table, or updating the row if it already exists in the table. The action of updating or inserting has been described as "upsert".

The way this is handled in PostgreSQL is by using the INSERT statement in combination with the ON CONFLICT clause.

### INSERT
The INSERT statement adds in new rows within the table. The values associated with specific target columns can be added in any order.

Let's look at a simple example. We will use a customer address table as an example, which is defined with the following CREATE statement:

    CREATE TABLE IF NOT EXISTS customer_address (
        customer_id int PRIMARY KEY, 
        customer_street varchar NOT NULL,
        customer_city text NOT NULL,
        customer_state text NOT NULL);

Let's try to insert data into it by adding a new row:

    INSERT into customer_address (
        VALUES (432, '758 Main Street', 'Chicago', 'IL');

    
Now let's assume that the customer moved and we need to update the customer's address. However we do not want to add a new customer id. In other words, if there is any conflict on the customer_id, we do not want that to change.

This would be a good candidate for using the **ON CONFLICT DO NOTHING** clause.

    INSERT INTO customer_address (customer_id, customer_street, customer_city, customer_state)
        VALUES
         (
         432, '923 Knox Street', 'Albany', 'NY'
         ) 
    ON CONFLICT (customer_id) 
    DO NOTHING;

Now, let's imagine we want to add more details in the existing address for an existing customer. This would be a good candidate for using the **ON CONFLICT DO UPDATE** clause.

    INSERT INTO customer_address (customer_id, customer_street)
    VALUES
        (
        432, '923 Knox Street, Suite 1' 
    ) 
    ON CONFLICT (customer_id) 
    DO UPDATE
        SET customer_street  = EXCLUDED.customer_street;


--- 
## NoSql Databases

No sql equals *Not only SQL* 

**Eventual Consistency:**

Over time (if no new changes are made) each copy of the data will be the same, but if there are new changes, the data may be different in different locations. The data may be inconsistent for only milliseconds. There are workarounds in place to prevent getting stale data.

**Is data deployment strategy an important element of data modeling in Apache Cassandra?**
Deployment strategies are a great topic, but have very little to do with data modeling. Developing deployment strategies focuses on determining how many clusters to create or determining how many nodes are needed. These are topics generally covered under database architecture, database deployment and operations, which we will not cover in this lesson. Here is a useful link to learn more about it for Apache Cassandra.

In general, the size of your data and your data model can affect your deployment strategies. You need to think about how to create a cluster, how many nodes should be in that cluster, how to do the actual installation. More information about deployment strategies can be found on this [DataStax documentation page](https://docs.datastax.com/en/dse-planning/doc/)

**CAP Theorem**

A theorem in computer science that states it is **impossible** for a distributed data store to **simultaineoulst provide** more than two out of the following thress guarntees of **consistency, availability,** and **partition tolerance**. 

__CAP Theorem__:

- **Consistency**: Every read from the database gets the latest (and correct) piece of data or an error

- **Availability**: Every request is received and a response is given -- without a guarantee that the data is the latest update

- **Partition Tolerance**: The system continues to work regardless of losing network connectivity between nodes

**Data Modeling in Apache Cassandra:**

- Denormalization is not just okay -- it's a must
- Denormalization must be done for fast reads
- Apache Cassandra has been optimized for fast writes
- ALWAYS think Queries first
- One table per query is a great strategy
- Apache Cassandra does not allow for JOINs between tables


**Primary Key**
- Must be unique
- The PRIMARY KEY is made up of either just the PARTITION KEY or may also include additional CLUSTERING COLUMNS
- A Simple PRIMARY KEY is just one column that is also the PARTITION KEY. A Composite PRIMARY KEY is made up of more than one column and will assist in creating a unique value and in your retrieval queries
- The PARTITION KEY will determine the distribution of data across the system

**Clustering Columns:**
- The clusting column will sort the data in sorted **ascending** order, e.g. alphabetical order
- More than one clusting column can be added (or none).
- From there the clusting coumns will sort in order of how they were added to the primary key. 

`CREATE TABLE... PRIMARY KEY (partition key1, clustering column1)`
`CREATE TABLE... PRIMARY KEY ((partition key1, partition key2), clustering column1, clustering column2)`

Behind these names ...

- The Partition Key is responsible for data distribution across your nodes.
- The Clustering Key is responsible for data sorting within the partition.
- The Primary Key is equivalent to the Partition Key in a single-field-key table (i.e. Simple).
- The Composite/Compound Key is just any multiple-column key

More examples:

`PRIMARY KEY (a)`: The partition key is `a`.
`PRIMARY KEY (a, b)`: The partition key is `a`, the clustering key is `b`.
`PRIMARY KEY ((a, b))`: The composite partition key is `(a, b)`.
`PRIMARY KEY (a, b, c)`: The partition key is `a`, the composite clustering key is `(b, c)`.
`PRIMARY KEY ((a, b), c)`: The composite partition key is `(a, b`), the clustering key is `c`.
`PRIMARY KEY ((a, b), c, d)`: The composite partition key is `(a, b)`, the composite clustering key is `(c, d)`.

**WHERE clause**
Data Modeling in Apache Cassandra is query focused, and that focus needs to be on the WHERE clause
Failure to include a WHERE clause will result in an error

 - Where Clause would be the Primary key first.  Then any additional Clustering keys in the order they were setup. 

