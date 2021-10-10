-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS cookies;
DROP TABLE IF EXISTS recipeLines;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS pallets;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS deliveredAmounts;

PRAGMA foreign_keys=ON;

CREATE TABLE cookies (
    cookie_name    TEXT UNIQUE PRIMARY KEY
);

CREATE TABLE recipeLines (
    recipe_id       TEXT UNIQUE PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    recipe_quantity INT,
    ingredient_name TEXT REFERENCES ingredients(ingredient_name),
    cookie_name     TEXT REFERENCES cookies(cookie_name)
);

CREATE TABLE ingredients (
    ingredient_name     TEXT UNIQUE PRIMARY KEY,
    quantity            INT,
    unit                TEXT,
    date                DATE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pallets (
    pallet_id       TEXT UNIQUE PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    cookie_name     TEXT REFERENCES cookies(cookie_name),
    order_id        TEXT REFERENCES orders(order_id),
    production_date DATE DEFAULT (DATE('now')),
    blocked         BOOLEAN DEFAULT 0
);

CREATE TABLE orders (
    order_id        TEXT UNIQUE PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    order_date      DATE,
    delivery_date   DATE,
    customer_id     TEXT REFERENCES customers(customer_id)
);

CREATE TABLE customers (
    customer_id TEXT UNIQUE PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    name        TEXT,
    address     TEXT
);

CREATE TABLE deliveredAmounts (
    delivery_id     TEXT UNIQUE PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    order_quantity  INT,
    cookie_name     TEXT REFERENCES cookies(cookie_name),
    order_id        TEXT REFERENCES orders(order_id)
);

INSERT
INTO    customers(name, address)
VALUES
    ("Finkakor AB", "Helsingborg"),
    ("Småbröd AB", "Malmö"),
    ("Kaffebröd AB", "Landskrona"),
    ("Bjudkakor AB", "Ystad"),
    ("Kalaskakor AB", "Trelleborg"),
    ("Partykakor AB", "Kristianstad"),
    ("Gästkakor AB", "Hässleholm"),
    ("Skånekakor AB", "Perstorp");

INSERT
INTO    cookies(cookie_name)
VALUES
    ("Nut ring"),
    ("Nut cookie"),
    ("Amneris"),
    ("Tango"),
    ("Almond delight"),
    ("Berliner");

INSERT
INTO ingredients(ingredient_name, quantity, unit)
VALUES
    ("Flour", 100000, "g"),
    ("Butter", 100000, "g"),
    ("Icing sugar", 100000, "g"),
    ("Roasted, chopped nuts", 100000, "g"),
    ("Fine-ground nuts", 100000, "g"),
    ("Ground, roasted nuts", 100000, "g"),
    ("Bread crumbs", 100000, "g"),
    ("Sugar", 100000, "g"),
    ("Egg whites", 100000, "ml"),
    ("Chocolate", 100000, "g"),
    ("Marzipan", 100000, "g"),
    ("Eggs", 100000, "g"),
    ("Potato starch", 100000, "g"),
    ("Wheat flour", 100000, "g"),
    ("Sodium bicarbonate", 100000, "g"),
    ("Vanilla", 100000, "g"),
    ("Chopped almonds", 100000, "g"),
    ("Cinnamon", 100000, "g"),
    ("Vanilla sugar", 100000, "g");

INSERT
INTO recipeLines(cookie_name, ingredient_name, recipe_quantity)
VALUES
    ("Nut ring", "Flour", 450),
    ("Nut ring", "Butter", 450),
    ("Nut ring", "Icing sugar", 190),
    ("Nut ring", "Roasted, chopped nuts", 225),
    ("Nut cookie", "Fine-ground nuts", 750),
    ("Nut cookie", "Ground, roasted nuts", 625),
    ("Nut cookie", "Bread crumbs", 125),
    ("Nut cookie", "Sugar", 375),
    ("Nut cookie", "Egg whites", 350),
    ("Nut cookie", "Chocolate", 50),
    ("Amneris", "Marzipan", 750),
    ("Amneris", "Butter", 250),
    ("Amneris", "Eggs", 250),
    ("Amneris", "Potato starch", 25),
    ("Amneris", "Wheat flour", 25),
    ("Tango", "Butter", 200),
    ("Tango", "Sugar", 250),
    ("Tango", "Flour", 300),
    ("Tango", "Sodium bicarbonate", 4),
    ("Tango", "Vanilla", 2),
    ("Almond delight", "Butter", 400),
    ("Almond delight", "Sugar", 270),
    ("Almond delight", "Chopped almonds", 279),
    ("Almond delight", "Flour", 400),
    ("Almond delight", "Cinnamon", 10),
    ("Berliner", "Flour", 350),
    ("Berliner", "Butter", 250),
    ("Berliner", "Icing sugar", 100),
    ("Berliner", "Eggs", 50),
    ("Berliner", "Vanilla sugar", 5),
    ("Berliner", "Chocolate", 50);