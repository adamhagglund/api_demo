# This is a small project to showcase API via the Python framework Bottle.


## Relations

The ER-model above gives the following relations.
Bold face for primary keys, italicized face for
foreign keys, and bold italicized face for attributes which
are both primary keys and foreign keys:

+ ingredients(**ingredient_name**, quantity, unit, date)
+ recipeLines(**recepie_id**, _cookie_name_, _ingredient_name_, recepie_quantity)
+ cookies(**cookie_name**)
+ pallets(**pallet_id**, _order_id_, _cookie_name_, ship_date, blocked, produced, location)
+ orders(**order_id**, _customer_id_, delivery_date)
+ customers(**customer_id**, name, address)
+ deliveredAmount(**delivery_id**, _cookie_id_, _order_id_, order_quantity)

## Requires
- Bottle (pip install Bottle)
- request (pip install requests)

## Scripts to set up database

The scripts used to set up and populate the database are in:

 + [`create-schema.sql`](create-schema.sql) (defines the tables), and (inserts data).

So, to create and initialize the database, we run:

```shell
sqlite3 name.db < create-schema.sql
```

(Choose _name_ to whatever you want to call your database file).

## How to compile and run the program

This section should give a few simple commands to type to
compile and run the program from the command line, such as:

```shell
python3 api.py
```
