# DATA WAREHOUSE

Simple definition:
> A data warehouse is a copy of transaction data specifically structured for query and analysis. 

Less simple definition: 
> A data warehouse is a system that rerieves and consolidates data periodically from the source systems into a dimensional or normalized data store. it usually keeps years of history and is queried for business intelligence or other analytical activities. It is typically updated in batches, not every time a transaction happens in the source system. 


### Architecture

**Kimball's Bus Architecture**

`Source data -> Back room -> Front Room <- applications and reports`

Starts with ETL behind the scenes.  

Source data is loaded into the back room where it is transformed and loaded into the front room. 

Front room
- Dimensional
- Atomic & summart data 
- Organized by business process
- Uses conformed dimensions 

Goals
- Ease of use 
- query performance 

**Independent Data Mart**

Similar to the Kimball's bus model, but each department has it's own ETL process for it's front room. 
- These separate and smaller dimensional models are called "Data Marts"
- Different fact tables for the same events, no confirmed dimensions 
- Uncoordinated efforts can lead to **inconsistent views**
- In larger organizations coordination on a single data mart can create considerable overhead. However it is generally discouraged. 

**Inmon's Corporate Information Factory** 

Acquire data from diparate sources into a 3NF DataWarehouse first. Then create independent data marts from that.  Creates better consistancy across departments when aggregation methods match. 

Applications can get data from the data marts or the original data warehouse. 

### OLAP Cubes

- An OLAP cube is a aggregation of a fact metic on a number of dimensions
- E.g. Movie, Branch, Month
- Easy to communicate to business users
- Common OLAP operations include: Rollup, drill-down, slice, & dice

SQL command to create a cube: 

`GROUP BY grouping sets ((), month, country, (month, country))`

Instead:

`GROUP BY cube(movie, branch, month)`

!!Be sure there are no None or Null data before grouping!! 

The results will return multiple combinations of the data. 


Links to the three books referenced in the video:

- [The Data Warehouse Toolkit: The Complete Guide to Dimensional Modeling (Kimball)](https://www.amazon.com/Data-Warehouse-Toolkit-Complete-Dimensional/dp/0471200247)
- [Building the Data Warehouse (Inmon)](https://www.amazon.com/Building-Data-Warehouse-W-Inmon/dp/0764599445)
- [Building a Data Warehouse: With Examples in SQL Server (Rainardi)](https://www.amazon.com/Building-Data-Warehouse-Examples-Experts/dp/1590599314)


# Cloud Computing - Redshift

Columnar Storage - Massively Parralelized - 

**Optimizing Table Design**

- When a table is partitioned up into many peices and distribued across slices in different machines, this is done blindly.
- If one has an idea about the frequent pattern of a table, one can choose a more clever strategy
- The 2 possible strategies are:
- - Distribution style 
- - Sorting key 


**Dist Key**

- EVEN Distributions - Attempts to evenly split all rows across the partitions, good if a table won't be joined. 
- ALL Distribution - Data replicated on all partitions. Great for small dimension tables to reduce shuffling. 
- AUTO Distribution - Leave the decision to Redshift. 
- KEY Distribution - Rows having similar values are placed in the same slice. 

High cost of join with EVEN distribution = Shuffling. 

**Sort Key**

Great for columns that will often be sorted by. 

- Defined in set up. 
- Redshift sorts rows before uploading 
- Reduces query time, but increases insert time. 

Great for Date dimension as it is always sorted. Then also sort the corresponding Foreign key in the fact table. 

