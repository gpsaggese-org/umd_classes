---
title: "06.1: MongoDB"
---

<!-- git_hash=b1afff2a-lhr timestamp=20260804_162414 -->

<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides001.png){width=80%}

</center>
<center>

# 2 / 16: Key-Value Store vs Document DBs

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides002.png){width=80%}

</center>
- **Key-Value Stores**
  - These databases function like a map or dictionary, where each key is associated with a specific value.
    - *Examples include HBase and Redis.*
  - They are optimized for retrieving values using keys, making them very fast for lookups.
  - Occasionally, they allow searching within value fields using patterns, but this is not their primary function.
  - Values are stored as uninterpreted data, such as binary blobs, which means the database does not understand the content of the values.
  - All key-value pairs exist within a single namespace, simplifying the structure but limiting complex queries.

- **Document DBs**
  - In these databases, key-value pairs are grouped into _documents_, which
    provide more structure.
    - _Examples include MongoDB and CouchDB._
  - Documents are formatted in JSON, XML, or BSON, allowing for more complex
    data representation.
  - Documents are organized into _collections_, similar to tables in relational
    databases, which helps in managing related data.
  - Large collections can be partitioned and indexed, improving performance for
    large datasets and complex queries.

<center>

# 3 / 16: MongoDB

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides003.png){width=80%}

</center>
- **Developed by MongoDB Inc**
  - Founded in 2007, MongoDB Inc. was established to address the challenges of handling large-scale data, drawing from the experiences of DoubleClick, a company known for its advertising services.
  - The name "Mongo" is derived from the word "humongous," reflecting its capability to manage vast amounts of data.

- **Highly popular NoSQL database**
  - **Document-oriented NoSQL DB**
    - MongoDB is schema-less, meaning it doesn't require a predefined structure
      like traditional SQL databases. This flexibility allows developers to
      store data in a way that best suits their applications.
    - Instead of using a Data Definition Language (DDL), MongoDB stores data as
      maps with any keys and values, and the application itself manages the
      schema.
    - Each document in MongoDB has a unique identifier, `_id`, which is
      automatically reserved by the database.
    - Data is stored in BSON format, which is a binary representation of JSON,
      allowing for efficient data storage and retrieval.

- **High-performance**
  - MongoDB is developed in C++, which contributes to its high performance and
    efficiency.
  - It supports APIs (drivers) in various programming languages, making it
    versatile and accessible for developers using languages like JavaScript,
    Python, Ruby, Java, Scala, and C++. This wide range of support enhances its
    usability across different platforms and applications.

<center>

# 4 / 16: MongoDB: Example of Document

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides004.png){width=80%}

</center>
- **MongoDB: Example of Document**
  - A document in MongoDB is structured as a *JSON data structure*. This means it uses a format that is easy to read and write for humans and machines. JSON stands for JavaScript Object Notation and is widely used for data interchange.

- **Corresponds to a Row in a Relational DB**
  - In traditional relational databases, data is stored in tables with rows and
    columns. In MongoDB, a document is similar to a row in these tables.
  - **Without Schema**: Unlike relational databases, MongoDB does not require a
    predefined schema. This allows for flexibility as each document can have
    different fields.
  - **Primary Key is `_id`**: Each document has a unique identifier called
    `_id`. This acts like a primary key in relational databases, ensuring each
    document can be uniquely identified.
  - **Values can be Nested**: MongoDB allows for complex data structures by
    supporting nested documents. This means values can be arrays or other
    documents, allowing for a rich representation of data.

<center>

# 5 / 16: MongoDB: Functionalities

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides005.png){width=80%}

</center>
- **MongoDB: Functionalities**
  - **Design goals**
    - *Performance*: MongoDB is designed to be fast and efficient, making it suitable for applications that require quick data access and processing.
    - **Availability/scalability**: It is built to handle large amounts of data and users, ensuring that the system remains available and responsive even as demand grows.
    - **Rich data storage (not rich querying!)**: While MongoDB excels at storing complex data structures, it does not focus on providing advanced querying capabilities like some other databases.

- **Dynamic schema**
  - _No DDL_: MongoDB does not require a fixed schema, allowing for flexibility
    in how data is stored and modified without needing to define a structure
    beforehand.
  - **Secondary indexes**: These are used to improve query performance by
    allowing quick access to data based on non-primary key fields.
  - **Query language via API**: MongoDB provides a way to interact with the
    database using a query language through its API, making it accessible for
    developers.

- **Several levels of data consistency**
  - _Atomic writes and fully-consistent reads (document level)_: MongoDB ensures
    that operations on a single document are atomic, meaning they are completed
    fully or not at all, and reads are consistent at the document level.

- **No joins nor transactions across multiple documents**
  - _Distributed queries easy and fast_: By avoiding complex operations like
    joins and multi-document transactions, MongoDB can perform distributed
    queries more efficiently, which is beneficial for scalability.

- **High availability through replica sets**
  - _Primary replication with automated failover_: MongoDB uses replica sets to
    ensure data is replicated across multiple servers, providing high
    availability and automatic failover in case of server failure.

- **Built-in sharding**
  - _Horizontal scaling via automated range-based partitioning_: Sharding allows
    MongoDB to distribute data across multiple servers, enabling horizontal
    scaling by partitioning data into ranges.
  - **Reads and writes distributed over shards**: This ensures that both read
    and write operations can be spread across different shards, improving
    performance and scalability.

<center>

# 6 / 16: MongoDB: Hierarchical Objects

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides006.png){width=80%}

</center>
- **Mongo Instance**
  - A MongoDB instance can contain multiple databases, similar to how a Postgres instance operates. This is the top level of the hierarchy in MongoDB.

- **Mongo Database**
  - Each database within an instance can have multiple collections. This is
    analogous to a Postgres database, which contains tables.

- **Mongo Collection**
  - Collections are similar to tables in relational databases like Postgres.
    They hold multiple documents, which are akin to rows in a table.

- **Mongo Document**
  - Documents are the basic unit of data in MongoDB, similar to rows in
    Postgres. Each document contains fields, which are comparable to columns in
    a table. Every document has a unique primary key, `_id`, which ensures each
    document can be uniquely identified.

- **Fields**
  - Fields within a document store the actual data and are similar to columns in
    a relational database. They can hold various data types and structures,
    allowing for flexible data modeling.

<center>

# 7 / 16: Relational DBs vs MongoDB: Concepts

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides007.png){width=80%}

</center>
* **Relational DBs vs MongoDB: Concepts**

- **Database vs Database**
  - In both relational databases (RDBMS) and MongoDB, a _database_ serves as a
    container. In RDBMS, it holds tables, while in MongoDB, it contains
    collections.

- **Relation/Table/View vs Collection**
  - A _collection_ in MongoDB is similar to a table in RDBMS. It groups
    documents, which are akin to rows in a table.

- **Row/Instance vs Document**
  - A _document_ in MongoDB is a set of fields, similar to a row in a relational
    database. Each document can have a unique structure.

- **Column/Attribute vs Field**
  - A _field_ in MongoDB is a name-value pair, comparable to a column in RDBMS.

- **Index vs Index**
  - Indexing in MongoDB is automatic, helping to speed up queries, similar to
    indexing in relational databases.

- **Primary Keys vs `_id` Field**
  - The `_id` field in MongoDB is always the primary key, ensuring each document
    is uniquely identifiable.

- **Foreign Key vs Reference**
  - _References_ in MongoDB act like foreign keys, pointing to documents in
    other collections.

- **Table Joins vs Embedded Documents**
  - Instead of table joins, MongoDB uses _embedded documents_, allowing nested
    structures within a document for related data.

* **Example Document Explanation**
  - The JSON-like structure shown is a MongoDB document.
  - **`_id`**: Unique identifier for the document.
  - **`country`**: Uses a reference to another collection, similar to a foreign
    key.
  - **`famous_for`**: An array of strings, showing flexibility in data types.
  - **`last_census`**: Stores a date as a string.
  - **`mayor`**: An embedded document, demonstrating nested data.
  - **`name`, `population`, `state`**: Simple fields with straightforward data
    types.

<center>

# 8 / 16: Relational vs Document DB: Workflows

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides008.png){width=80%}

</center>
* **Relational DBs**
  - *E.g., PostgreSQL*: This is a popular example of a relational database, which organizes data into tables.
  - **Know what to store**: Relational databases are best for *tabular data*, meaning data that fits neatly into rows and columns.
  - **Static schema allows query flexibility**: A *static schema* means the structure of the database is defined before data is entered. This allows for complex queries, like *joins*, which combine data from different tables.
  - **Complexity at insertion time**: When adding data, you must decide how it fits into the predefined *schema*. This can be complex because you need to plan how data will be structured and related.

- **Document DBs**
  - _E.g., MongoDB_: This is a well-known document database, which stores data
    in a flexible, JSON-like format.
  - **No assumptions on storage**: Document databases can handle _irregular JSON
    data_, meaning data that doesn't fit neatly into tables.
  - **Access data by key**: Data is stored in a _nested key-value map_, which
    means you retrieve data using keys, similar to how you would access values
    in a dictionary.
  - **Complexity at access time**: The challenge here is when you _retrieve data
    from the server_. You often need to _process data client-side_, which can be
    complex if the data structure is irregular or deeply nested.

<center>

# 9 / 16: Why Use MongoDB?

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides009.png){width=80%}

</center>
- **Simple and powerful to query**
  - MongoDB offers a straightforward querying process, making it easy for developers to interact with the database. This simplicity is beneficial for rapid development and iteration.

- **Fast**
  - MongoDB is noted to be 2-10 times faster than PostgreSQL. This speed
    advantage is crucial for applications requiring quick data retrieval and
    processing, enhancing user experience and system performance.

- **Data model suitable for most web applications**
  - _Semi-structured data_: MongoDB's flexible schema allows for storing
    semi-structured data, which is common in web applications where data formats
    can vary.
  - _Quickly evolving systems_: The adaptability of MongoDB's data model
    supports systems that need to evolve rapidly, accommodating changes without
    significant restructuring.

- **Not suited for heavy, complex transaction systems**
  - While MongoDB excels in speed and flexibility, it may not be ideal for
    systems requiring complex transactions, such as banking systems, where data
    integrity and transaction management are critical.

The accompanying chart visually demonstrates MongoDB's superior performance in
terms of inserts and queries per second compared to SQL databases, highlighting
its efficiency in handling large volumes of operations.

<center>

# 10 / 16: MongoDB: Data Model

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides010.png){width=80%}

</center>
- **Documents as Field-Value Pairs**:
  - In MongoDB, data is stored in *documents*, which are composed of field-value pairs.
  - **Field Names**: These are strings that act as keys in the document.
  - **Values**: Can be of any BSON type, which includes:
    - Arrays of documents: Allows for nested data structures.
    - Native data types: Such as strings, numbers, and booleans.
    - Other documents: Enables embedding documents within documents for complex data models.

- **Examples**:
  - **\_id**: This is a unique identifier for each document, typically an
    `ObjectId`.
  - **name**: A document containing fields like `first` and `last` to store
    names.
  - **birth and death**: Dates are stored using the date type, allowing for
    date-specific operations.
  - **contribs**: An array of strings, useful for storing lists of contributions
    or tags.
  - **views**: Uses `NumberLong` type for storing large numbers, such as view
    counts.

These examples illustrate how MongoDB's flexible schema allows for a variety of
data types and structures, making it suitable for diverse applications.

<center>

# 11 / 16: MongoDB: Data Model

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides011.png){width=80%}

</center>
- **Documents can be nested**
  - *Embedded sub-document*: In MongoDB, documents can contain other documents, known as embedded sub-documents. This allows for a hierarchical data structure within a single document, making it easier to store related data together.

- **Denormalized data models**
  - _Store related information in the same record_: Denormalization involves
    storing related data in a single document. This approach reduces the need
    for complex queries and improves read performance by avoiding joins.
  - _Avoids the need for a join operation_: By keeping related data together,
    denormalized models eliminate the need for join operations, which can be
    costly in terms of performance.

- **Normalized data models**
  - _Eliminate duplication_: Normalization involves structuring data to minimize
    redundancy. This is achieved by separating data into different documents and
    linking them through references.
  - _Represent many-to-many relationships_: Normalized models are useful for
    representing complex relationships, such as many-to-many, by using
    references between documents. This approach can make updates more efficient
    by reducing data duplication.

<center>

# 12 / 16: Schema Free

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides012.png){width=80%}

</center>
* **Schema Free**
  - **MongoDB does not need pre-defined data schema**
    - MongoDB is a NoSQL database, which means it doesn't require a fixed schema. This flexibility allows developers to store data without defining the structure beforehand, unlike traditional relational databases.

- **Every _document_ in a _collection_ can have different fields and values**
  - Each document in MongoDB can have its own unique set of fields and data
    types. This means you don't have to worry about `NULL` values or creating a
    union of fields as you would in a relational database. This flexibility is
    particularly useful for applications where data structures can evolve over
    time.

- **E.g., heterogeneous data instances**
  - The image illustrates various documents with different fields and values.
    For example, one document might include fields like `name`, `eyes`, and
    `birthplace`, while another might only have `name` and `hat`. This
    demonstrates MongoDB's ability to handle diverse data types and structures
    within the same collection, making it ideal for applications with varying
    data requirements.

<center>

# 13 / 16: JSON Format

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides013.png){width=80%}

</center>
- **JSON Format**
  - JSON stands for *JavaScript Object Notation*. It's a lightweight format used for data interchange. It's easy for humans to read and write, and easy for machines to parse and generate.
  - **Data is stored in field/value pairs**
    - Each piece of data in JSON is represented as a field/value pair. This is similar to a dictionary or a map in programming.
    - **A field/value pair consists of:**
      - A field name, which is always a string. This acts like a label for the data.
      - A colon `:` separates the field name from its value.
      - A typed value follows the colon. This value can be a string, number, object, array, true, false, or null.
      - Example: `"name": "R2-D2"` shows a field named "name" with the value "R2-D2".

- **Data in documents is separated by commas `,`**
  - When you have multiple field/value pairs in a JSON document, they are
    separated by commas.
  - Example: `"name": "R2-D2", "race": "Droid"` shows two pairs separated by a
    comma.

- **Curly braces `{}` hold documents**
  - A JSON document is enclosed in curly braces. This is similar to how objects
    are defined in many programming languages.
  - Example: `{ "name": "R2-D2", "race": "Droid", "affiliation": "rebels" }` is
    a complete JSON object with three field/value pairs.

- **An array is stored in brackets `[]`**
  - JSON can also represent arrays, which are ordered lists of values. Arrays
    are enclosed in square brackets.
  - Each item in the array can be a JSON object, like in the example.
  - Example: The array
    `[ { "name": "R2-D2", "race": "Droid", "affiliation": "rebels" }, { "name": "Yoda", "affiliation": "rebels" } ]`
    contains two JSON objects.

<center>

# 14 / 16: BSON Format

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides014.png){width=80%}

</center>
* **BSON Format**
  - *Binary-encoded serialization of JSON-like documents*
    - BSON stands for Binary JSON. It is a way to encode data structures that are similar to JSON but in a binary format. This makes it more efficient for computers to read and write compared to plain text JSON. You can find more details about BSON at [bsonspec.org](https://bsonspec.org).
    - BSON is somewhat like Protocol Buffers, which is another way to serialize data. However, BSON is more flexible because it doesn't require a predefined schema. This means you can store different types of data without having to define the structure beforehand.

- **Optimized for random access**
  - BSON is designed to allow quick access to data. Each element in a BSON
    document is prefixed with a length field. This means that you can easily
    skip over elements without having to read everything, which is useful when
    you only need to access specific parts of the data.

- **MongoDB understands BSON objects, even nested ones**
  - MongoDB, a popular database, uses BSON to store data. It can handle BSON
    objects that contain other BSON objects inside them, known as nested
    objects. MongoDB can create indexes on these BSON keys, which helps in
    quickly finding and retrieving data based on queries. This capability makes
    MongoDB efficient for handling complex data structures.

<center>

# 15 / 16: ObjectID

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides015.png){width=80%}

</center>
- **Each JSON document contains an `_id` field of type `ObjectId`**
  - This is similar to the *SERIAL* constraint in PostgreSQL, which automatically increments a numeric primary key. In MongoDB, the `_id` field is automatically generated and serves as a unique identifier for each document.

- **An `ObjectId` is 12 bytes, composed of:**
  - **Timestamp**: The first part of the `ObjectId` is a timestamp, which
    ensures that the IDs are roughly ordered by creation time.
  - **Client machine ID**: This part identifies the machine where the `ObjectId`
    was generated, helping to ensure uniqueness across different machines.
  - **Client process ID**: This identifies the process on the machine, further
    ensuring that IDs are unique even if multiple processes are generating them.
  - **3-byte auto-incremented counter**: This counter is unique to each process
    and resets every second, ensuring that even within the same second, IDs
    remain unique.

- **Each MongoDB process handles its own ID generation without collisions**
  - MongoDB's distributed nature means that multiple servers can generate IDs
    independently without risk of duplication, thanks to the components of the
    `ObjectId`.

- **Details**
  - For more in-depth information, you can refer to the
    [MongoDB documentation](https://www.mongodb.com/docs/manual/reference/bson-types/#objectid),
    which provides comprehensive details on how `ObjectId` works and its
    components.

<center>

# 16 / 16: Indexes

</center>
<center>

![](data605/lectures_commentary/Lesson06.1-MongoDB.png/slides016.png){width=80%}

</center>
* **Indexes**
  - **Primary index**
    - This is an index that is automatically created on the `_id` field of a database. The `_id` field is a unique identifier for each document in a collection, similar to a primary key in SQL databases. The primary index uses a B+ tree structure, which is efficient for searching and retrieving data quickly.

- **Secondary index**
  - Secondary indexes are additional indexes that you can create to improve the
    performance of queries. They are not automatically created like the primary
    index. Secondary indexes can also enforce unique values for a specific
    field, ensuring that no two documents have the same value for that field.

- **Single field index and compound index (like SQL)**
  - A single field index is created on one field, while a compound index
    involves multiple fields. The order of fields in a compound index is
    important because it affects how queries are optimized and executed. This is
    similar to how indexes work in SQL databases.

- **Sparse property of an index**
  - A sparse index only includes entries for documents that have the indexed
    field. If a document does not have the field, it is ignored by the index.
    This can save space and improve performance when indexing fields that are
    not present in every document.

- **Rejects records with duplicate keys if the index is unique and sparse**
  - If an index is both unique and sparse, it will reject any records that would
    result in duplicate keys. This ensures data integrity by preventing
    duplicate entries for the indexed field.

- **Details [here](https://www.mongodb.com/docs/manual/indexes/)**
  - For more detailed information about indexes, you can refer to the official
    MongoDB documentation. This resource provides comprehensive guidance on how
    to use and manage indexes effectively.
