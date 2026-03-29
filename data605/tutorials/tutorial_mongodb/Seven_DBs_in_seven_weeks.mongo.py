# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## Functions

# %%
# #!pip3 install rich

import pprint


# %% [markdown]
# # Connect to DB

# %%
import pymongo


def print_(cursor, mode="pprint", tag=""):
    """
    Print collection.
    """
    if tag:
        print("%s=" % tag)
    if isinstance(cursor, pymongo.cursor.Cursor):
        # Serialize a cursor into a list.
        obj = list(cursor)
    else:
        obj = cursor
    if mode in ("json", "json_color"):
        import json

        parsed = json.loads(json.dumps(obj))
        if mode == "json":
            print(json.dumps(parsed, indent=2))
        else:
            import rich

            rich.print_json(json.dumps(parsed, indent=2))
    elif mode == "pprint":
        pprint.pprint(obj)
    else:
        raise ValueError(f"Invalid mode='{mode}'")


from bson.objectid import ObjectId

# Connect to MongoDB instance.
client = pymongo.MongoClient("localhost", 27017)

# Create a Mongo database.
db = client["book"]
print("db=", db)
print("type(db)=", type(db))

# %%
# Show all the collections in the DB.
print("collections=", db.list_collection_names())

# Clean all the collections.
for collection_name in db.list_collection_names():
    print("Dropping collection %s" % collection_name)
    db[collection_name].drop()

# Show all the collections in the DB.
print("collections=", db.list_collection_names())

# %% [markdown]
# # `Towns` collection

# %% [markdown]
# ## Insert

# %%
dict_ = {
    "name": "New York",
    "population": 22200000,
    "lastCensus": "2022-11-01",
    "famousFor": ["the MOMA", "food", "Derek Jeter"],
    "mayor": {"name": "Bill de Blasio", "party": "D"},
}
print_(dict_, tag="dict_")

# Inserting an object in a DB creates a DB.
val = db.towns.insert_one(dict_)
print("val=", val)
print("obj_id=", val.inserted_id)
print(dir(val))

# %%
# Show all the collections.
db.list_collection_names()

# %%
# Scan the collection.
for obj in db.towns.find():
    # _id is like the primary key.
    print_(obj, mode="pprint")


# %%
# Insert more data in the collection.
def insert_city(name, population, lastCensus, famousFor, mayor):
    db.towns.insert_one(
        {
            "name": name,
            "population": population,
            "lastCensus": lastCensus,
            "famousFor": famousFor,
            "mayor": mayor,
        }
    )


insert_city(
    "Punxsutawney",
    6200,
    "2016-01-31",
    ["Punxsutawney Phil"],
    # mayor.
    {"name": "Richard Alexander"},
)

insert_city(
    "Portland",
    582000,
    "2016-09-20",
    ["beer", "food", "Portlandia"],
    # mayor.
    {"name": "Ted Wheeler", "party": "D"},
)

# Note that `mayor` field doesn't have a strict schema.

# %%
# Print all the documents in db["towns"].
for obj in db.towns.find():
    print_(obj, mode="pprint")

# %% [markdown]
# ## Query

# %%
# Find by ObjectId.
# db.towns.find_one({"_id": ObjectId("6368352a657571ee34691dd9")})
db.towns.find_one({"_id": val.inserted_id})

# %%
# Retrieve only the field `name` (i.e., projection).
object_id = ObjectId(str(val.inserted_id))
db.towns.find_one({"_id": object_id}, {"name": 1})

# %%
# Retrieve all fields excluding `name`.
db.towns.find_one({"_id": ObjectId(str(val.inserted_id))}, {"name": 0})

# %%
# Find all towns with name starting with P.
# This is going to do a table scan.
print_(db.towns.find({"name": {"$regex": r"^P"}}))

# %%
# Find all towns with name starting with P, but print only name.
print_(db.towns.find({"name": {"$regex": r"^P"}}, {"_id": 0, "name": 1}))

# %%
# Find all towns with name that begins with P and have population less than 100,000.
print_(db.towns.find({"name": {"$regex": r"^P"}, "population": {"$lt": 100000}}))

# %%
# Projection.
print_(
    db.towns.find({"famousFor": "food"}, {"_id": 0, "name": 1, "famousFor": 1})
)

# Note that the equality with an array is interpreted as "in".

# %%
# Query for matching values.
print_(
    db.towns.find(
        {"famousFor": {"$all": ["food", "beer"]}},
        {"_id": 0, "name": 1, "famousFor": 1},
    )
)

# %%
# Query for lack of matching values.
print_(
    db.towns.find(
        {"famousFor": {"$nin": ["food", "beer"]}},
        {"_id": 0, "name": 1, "famousFor": 1},
    )
)

# %%
# Find results with nested search criteria, e.g., mayor.party = "D".
print_(db.towns.find({"mayor.party": "D"}))

# %% [markdown]
# ## Updating

# %%
print_(db.towns.find())

# %%
# Find the ID for a given document.
object_id_for_Portland = str(db.towns.find_one({"name": "Portland"})["_id"])
print("object_id_for_Portland=", object_id_for_Portland)

# Note that types matter, so searching for an _id as string doesn't work.
# print_(db.towns.find_one({"_id": object_id_for_Portland}))
print_(db.towns.find_one({"_id": ObjectId(object_id_for_Portland)}))

# %%
# There are multiple cities called Portland in US (e.g., in Oregon and in Maine).
# So add the state.
db.towns.update_one(
    {"_id": ObjectId(object_id_for_Portland)}, {"$set": {"state": "OR"}}
)

print_(db.towns.find({"_id": ObjectId(object_id_for_Portland)}))

# Note that we need to specify $set.
# Mongo thinks in terms of documents and not attributes. So if you specify:
# db.towns.update_one({"_id": ObjectId("63696c28657571ee34691de3")},
#                     {"state": "OR"})
# the entire document will be replaced with the document `{"state": "OR"}`

# %%
# Increment the population.
db.towns.update_one(
    {"_id": ObjectId(object_id_for_Portland)}, {"$inc": {"population": 1000}}
)
print_(db.towns.find({"_id": ObjectId(object_id_for_Portland)}))

# %% [markdown]
# # `countries` collection

# %% [markdown]
# ## Insert

# %%
# Delete collection, if it exists.
db.countries.drop()

# Note that:
# 1) we define the _id directly
# 2) the schema is not strict
db.countries.insert_one(
    {
        "_id": "us",
        "name": "United States",
        "exports": {
            "foods": [{"name": "bacon", "tasty": True}, {"name": "burgers"}]
        },
    }
)

db.countries.insert_one(
    {
        "_id": "ca",
        "name": "Canada",
        "exports": {
            "foods": [
                {"name": "bacon", "tasty": False},
                {"name": "syrup", "tasty": True},
            ]
        },
    }
)

db.countries.insert_one(
    {
        "_id": "mx",
        "name": "Mexico",
        "exports": {
            "foods": [{"name": "salsa", "tasty": True, "condiment": True}]
        },
    }
)

assert db.countries.count_documents({}) == 3

# %%
for obj in db["countries"].find():
    print_(obj)

# %% [markdown]
# ## Query

# %%
# Find the country that exports tasty bacon.

# This doesn't return what we want, since we want the AND of the condition and not OR.
print_(
    db.countries.find(
        {
            "exports.foods.name": "bacon",
            "exports.foods.tasty": True,
        },
        {"_id": 0, "name": 1},
    )
)

# %%
# Using $elemMatch.
print_(
    db.countries.find(
        {
            "exports.foods": {
                "$elemMatch": {
                    "name": "bacon",
                    "tasty": True,
                }
            }
        },
        {"_id": 0, "name": 1},
    )
)

# %%
# This performs an AND.
print_(db.countries.find({"_id": "mx", "name": "United States"}))

# This performs an OR.
print_(
    db.countries.find(
        {"$or": [{"_id": "mx"}, {"name": "United States"}]}, {"_id": 1}
    )
)

# %% [markdown]
# ## References

# %%
object_id_for_Pun = ObjectId(
    str(db.towns.find_one({"name": "Punxsutawney"})["_id"])
)
print("object_id_for_Pun=", object_id_for_Pun)

# %%
# Mongo is not built to perform joins.
# It is useful to have documents reference each other.
db.towns.update_one(
    {"_id": object_id_for_Pun},
    {"$set": {"country": {"$ref": "countries", "$id": "us"}}},
)

print_(db.towns.find_one({"_id": object_id_for_Pun}))

# %%
var = db.towns.find_one({"_id": object_id_for_Pun})
print("var=", var)
print('var["country"]=', var["country"])
# Dereference.
print(var["country"].id)

# %% [markdown]
# ## Delete

# %%
# Find all contries where the bacon is not tasty.
bad_bacon = {
    "exports.foods": {
        "$elemMatch": {
            "name": "bacon",
            "tasty": False,
        }
    }
}
print_(db.countries.find(bad_bacon))

# %%
print_(db.countries.find())

# %%
print("count=", db.countries.count_documents({}))
db.countries.delete_many(bad_bacon)
print("count=", db.countries.count_documents({}))

# %% [markdown]
# ## Query with code

# %% [markdown]
# # Indexing

# %%
import random

random.seed(1)


def populatePhones(area, start, stop):
    for i in range(start, stop):
        country = 1 + random.randint(1, 8)
        num = int(country * 1e10 + area * 1e7 + i)
        # +4 800-5550000
        full_number = "+%s %s-%s" % (country, area, i)
        # print(num, full_number)
        # assert 0
        db.phones.insert_one(
            {
                "_id": num,
                "components": {
                    "country": country,
                    "area": area,
                    "number": i,
                },
                "display": full_number,
            }
        )


# Generate 100,000 phone numbers (it may take a while), between 1-800-555-0000 and 1-800-565-0000.
db.phones.drop()
populatePhones(800, 5550000, 5650000)

# %%
print(db.phones.count_documents({}))

# %%
print_(db.phones.find().limit(2))
print_(db.phones.find().limit(2))

# %%
# Print information about the indices.
for collection in db.list_collection_names():
    print("# collection=", collection)
    print_(db[collection].index_information())

# %%
print_(db.phones.find_one({"display": "+4 800-5550000"}))

# %%
# db.phones.find({"display": "+4 800-5550000"}).explain()
db.phones.find({"display": "+4 800-5550000"}).explain()["executionStats"][
    "executionTimeMillis"
]

# %%
# Create an indesx on `display`.
db.phones.create_index(
    [("display", pymongo.ASCENDING)], unique=True, dropDups=True
)

print_(db["phones"].index_information())

# %%
# Show that the query now it's very fast.
print_(
    db.phones.find({"display": "+4 800-5550000"}).explain()["executionStats"][
        "executionTimeMillis"
    ]
)

# %% [markdown]
# # Aggregated queries.

# %%
db.phones.count_documents({"components.number": {"$gt": 5599999}})

# %%
db.phones.distinct("components.number", {"components.number": {"$gt": 5599999}})[
    :10
]
