# Data Lakes with Spark

---

One of the most popular tools for analysing big data. 
--- 

What is Big data? 

The numbers everyone should know: 

**CPU (Central Processing Unit)**

### 0.4ns 2.5ghz = 2.5 billion operations per second

The CPU is the "brain" of the computer. Every process on your computer is eventually handled by your CPU. This includes calculations and also instructions for the other components of the compute.

**Memory (RAM)**

### 100ns

Memory takes about 250 times longer to find and load a random byte from memory.  
When your program runs, data gets temporarily stored in memory before getting sent to the CPU. Memory is ephemeral storage - when your computer shuts down, the data in the memory is lost.

**Storage (SSD or Magnetic Disk)**

### 16us 

Loading memory from magnetic disk can be about 200 times slower than Ram, SSD's about 15 times slower.
Storage is used for keeping data over long periods of time. When a program runs, the CPU will direct the memory to temporarily load data from long-term storage.

**Network (LAN or the Internet)**

### 50ms 

About 20 times longer to process data when moving from one machine to another.
Network is the gateway for anything that you need that isn't stored on your computer. The network could connect to other computers in the same room (a Local Area Network) or to a computer on the other side of the world, connected over the internet.

**NETWORK**  ---20x--->  **SSD**  ---15x--->  **MEMORY**  ---200x--->  **CPU**


[Peter Norvig post](http://norvig.com/21-days.html)

[Interactive version!](http://people.eecs.berkeley.edu/~rcs/research/interactive_latency.html)

--- 

## Should I use Spark? 

4 gbs or 200 gbs? 

When the challenge of spliting and sending data to multiple machines to be processed is faster than the paralysis when a single machine starts thrashing. 

**HADOOP** - Hadoop is the Framework of the distributed computing of Spark.

Some common vocab of the framework: 

- HDFS - Hadoop distributed framework storage
- MAP REDUCE - The processing of the data. Map the tasks. Shuffle to each computer. Reduce the chunks back into a single response
- YARN - Is the resource manager that schedules the conputational workload. 
- HADOOP COMMON - Libraries and utilities. 

**APACHE PIG and HIVE** - SQL for map reduce. But, both of these need to write results to disk. 

**APACHE SPARK**- Doesnt need to write to disk, Can produce in memory computations. 

**APACHE STORM and FLINK** - Streaming Data 

*How is Spark related to Hadoop?* 

Spark, which is the main focus of this course, is another big data framework. Spark contains libraries for data analysis, machine learning, graph analysis, and streaming live data. Spark is generally faster than Hadoop. This is because Hadoop writes intermediate results to disk whereas Spark tries to keep intermediate results in memory whenever possible.

### Spark Cluster 

How do the nodes know which tasks to run and in which order? 

Most nodes are organized into a master/worker architechture. 

There are 4 modes of Spark distribution. 

- **Local Mode**: Single machine to check syntax and test projects. 
- **Cluster Manager**:
- - Standalone
- - Yarn
- - Mesos

--- 
### **Spark Use Cases and Resources**

Here are a few resources about different Spark use cases:

- [Data Analytics](http://spark.apache.org/sql/)
- [Machine Learning](http://spark.apache.org/mllib/)
- [Streaming](http://spark.apache.org/streaming/)
- [Graph Analytics](http://spark.apache.org/graphx/)

### **You Don't Always Need Spark**
Spark is meant for big data sets that cannot fit on one computer. But you don't need Spark if you are working on smaller data sets. In the cases of data sets that can fit on your local computer, there are many other options out there you can use to manipulate data such as:

- [AWK](https://en.wikipedia.org/wiki/AWK) - a command line tool for manipulating text files
- [R](https://www.r-project.org/) - a programming language and software environment for statistical computing
- [Python PyData Stack](https://pydata.org/downloads.html), which includes pandas, Matplotlib, NumPy, and scikit-learn among other libraries

Sometimes, you can still use pandas on a single, local machine even if your data set is only a little bit larger than memory. Pandas can read data in chunks. Depending on your use case, you can filter the data and write out the relevant parts to disk.

If the data is already stored in a relational database such as [MySQL](https://www.mysql.com/) or [Postgres](https://www.postgresql.org/), you can leverage SQL to extract, filter and aggregate the data. If you would like to leverage pandas and SQL simultaneously, you can use libraries such as [SQLAlchemy](https://www.sqlalchemy.org/), which provides an abstraction layer to manipulate SQL tables with generative Python expressions.

The most commonly used Python Machine Learning library is [scikit-learn](http://scikit-learn.org/stable/). It has a wide range of algorithms for classification, regression, and clustering, as well as utilities for preprocessing data, fine tuning model parameters and testing their results. However, if you want to use more complex algorithms - like deep learning - you'll need to look further. [TensorFlow](https://www.tensorflow.org/) and [PyTorch](https://pytorch.org/) are currently popular packages.

### **Spark's Limitations**

Spark has some limitation.

Spark Streaming’s latency is at least 500 milliseconds since it operates on micro-batches of records, instead of processing one record at a time. Native streaming tools such as [Storm](http://storm.apache.org/), [Apex](https://apex.apache.org/), or [Flink](https://flink.apache.org/) can push down this latency value and might be more suitable for low-latency applications. Flink and Apex can be used for batch computation as well, so if you're already using them for stream processing, there's no need to add Spark to your stack of technologies.

Another limitation of Spark is its selection of machine learning algorithms. Currently, Spark only supports algorithms that scale linearly with the input data size. In general, deep learning is not available either, though there are many projects integrate Spark with Tensorflow and other deep learning tools.

### **Hadoop versus Spark**

The Hadoop ecosystem is a slightly older technology than the Spark ecosystem. In general, Hadoop MapReduce is slower than Spark because Hadoop writes data out to disk during intermediate steps. However, many big companies, such as Facebook and LinkedIn, started using Big Data early and built their infrastructure around the Hadoop ecosystem.

While Spark is great for iterative algorithms, there is not much of a performance boost over Hadoop MapReduce when doing simple counting. Migrating legacy code to Spark, especially on hundreds of nodes that are already in production, might not be worth the cost for the small performance boost.

### **Beyond Spark for Storing and Processing Big Data**

Keep in mind that Spark is not a data storage system, and there are a number of tools besides Spark that can be used to process and analyze large datasets.

Sometimes it makes sense to use the power and simplicity of SQL on big data. For these cases, a new class of databases, know as NoSQL and NewSQL, have been developed.

For example, you might hear about newer database storage systems like HBase or Cassandra. There are also distributed SQL engines like Impala and Presto. Many of these technologies use query syntax that you are likely already familiar with based on your experiences with Python and SQL.

In the lessons ahead, you will learn about Spark specifically, but know that many of the skills you already have with SQL, Python, and soon enough, Spark, will also be useful if you end up needing to learn any of these additional Big Data tools.


--- 

## Data Wrangling

- Start Spark Context - The main entry point that provides Spark functionality and connects the data with the application 

- Start Spark Conf - object that specifies information such as the app name and the master node IP address

- Start Spark Session - to read dataframes spark context spark sql equivalent SparkSession
- - .builder\
- - .appName\
- - .config()\
- - **.getOrCreate()**  - Import starter that will find or start a new spark session. 




- Load data (s3 or HDFS)

- 

## Functions



In the previous video, we've used a number of functions to manipulate our dataframe. Let's take a look at the different type of functions and their potential pitfalls.

**General functions**

We have used the following general functions that are quite similar to methods of pandas dataframes:

- `select()`: returns a new DataFrame with the selected columns
- `filter()`: filters rows using the given condition
- `where()`: is just an alias for `filter()`
- `groupBy()`: groups the DataFrame using the specified columns, so we can run aggregation on them
- `sort()`: returns a new DataFrame sorted by the specified column(s). By default the second parameter 'ascending' is True.
- `dropDuplicates()`: returns a new DataFrame with unique rows based on all or just a subset of columns
- `withColumn()`: returns a new DataFrame by adding a column or replacing the existing column that has the same name. The first parameter is the name of the new column, the second is an expression of how to compute it.

**Aggregate functions**

Spark SQL provides built-in methods for the most common aggregations such as count(), countDistinct(), avg(), max(), min(), etc. in the pyspark.sql.functions module. These methods are not the same as the built-in methods in the Python Standard Library, where we can find min() for example as well, hence you need to be careful not to use them interchangeably.

In many cases, there are multiple ways to express the same aggregations. For example, if we would like to compute one type of aggregate for one or more columns of the DataFrame we can just simply chain the aggregate method after a `groupBy()`. If we would like to use different functions on different columns,` agg()` comes in handy. For example `agg({"salary": "avg", "age": "max"})` computes the average salary and maximum age.

**User defined functions (UDF)**

In Spark SQL we can define our own functions with the udf method from the pyspark.sql.functions module. The default type of the returned variable for UDFs is string. If we would like to return an other type we need to explicitly do so by using the different types from the pyspark.sql.types module.

**Window functions**

Window functions are a way of combining the values of ranges of rows in a DataFrame. When defining the window we can choose how to sort and group (with the `partitionBy` method) the rows and how wide of a window we'd like to use (described by `rangeBetween` or `rowsBetween`).

For further information see
Spark SQL DataFrames and Datasets Guide - https://spark.apache.org/docs/latest/sql-programming-guide.html
Spark Python API Docs - https://spark.apache.org/docs/latest/api/python/index.html

## Debugging 

Running a spark Script - 

- Scripts should end in `spark.stop()`

- To run a script: find where spark is `which spark`

- Runnign a script.  Normally you would call the ip address of the master node, but on AWS EMR, yarn works. `usr/bin/spark-submit --master yarn ./myscript.py`

- Use a different protocol for s3 from EMR: 
```
df = spark.read.json("s3a://mybucket/mydata.json")
df.persist()

df.take(5)
```

Remember lazy evaluation

Acumulators - These are like global varibles for the entire cluster.  In debugging, If I set a print statement to see what a variabl looked like, it woudl print on the worker node that I can't see.  Thus, use acummulators. 

`incorrectRecords = spark.accumulator(0, 0)`

```
def add_incorrect_record():
    global incorrectRecords
    incorrectRecords += 1

from pyspark.spl import udf
correct_ts = udf(lambda x: 1 if x.isdigit() else add_incorrect_record())

.withcolumn('tsDigit', correct_ts(logs.ts))
```
Caution, accumulators can be misleading if they are run more than once. 

Port 8080 is the webui.

**Data Skew** = Big chunk of data comes from a small group if users. So, it forces computations onto a single machine. Drill down in the Spark UI to the task level you can see if certain partitions process significantly more data than others and if they are lagging behind
- partition differently
- Add an intermediate data processing step on an alternative key


# Data Lakes 

Schema on Read and clustered cheaper hardware is the main point.  We can store data as files and work with it like a database. The clustereed hardware make this work much cheaper on massive data

in AWS Spark notebook, remember to open a new notebook from the spark env.  Then %%spark should start a context. 

