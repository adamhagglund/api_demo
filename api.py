from bottle import get, post, run, request, response
import sqlite3
import json

HOST = 'localhost'
PORT = 8888
conn = sqlite3.connect("cookies.sqlite")


def url(resource):
    return f"http://{HOST}:{PORT}{resource}"


def format_response(d):
    return json.dumps(d, indent=4) + "\n"

@post('/reset')
def reset():
    script_execution('create-schema.sql')
    response.status = 200
    return format_response({"status" : "ok"})

@get('/customers')
def get_customers():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(    
        """
        SELECT name, address
        FROM   customers
        """
    )
    s = [{"name": name, "address": address}
         for (name, address) in c]
    response.status = 200
    return format_response({"customers" : s})
    
@get('/ingredients')
def get_ingredients():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT ingredient_name, quantity, unit
        FROM   ingredients
        """
    )
    s = [{"name": ingredient_name, "quantity": quantity, "unit": unit}
         for (ingredient_name, quantity, unit) in c]
    response.status = 200
    return format_response({"ingredients": s})

@get('/cookies')
def get_cookies():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute("""
        SELECT cookie_name
        FROM    cookies
        ORDER BY cookie_name
        """)
    s = [{"name" : cookie_name[0]}
         for (cookie_name) in c]
    response.status = 200
    return format_response({"cookies" : s})

@get('/recipes')
def get_recipes():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute("""
        SELECT  cookie_name, ingredient_name, recipe_quantity, unit
        FROM    cookies
        JOIN    recipeLines
        USING   (cookie_name)
        JOIN    ingredients
        USING   (ingredient_name)
        ORDER BY cookie_name, ingredient_name
        """)
    s = [{"cookie" : cookie_name, "ingredient" : ingredient_name, "quantity" : recipe_quantity, "unit" : recipe_unit}
         for (cookie_name, ingredient_name, recipe_quantity, recipe_unit) in c]
    response.status = 200
    return format_response({"recipes" : s})



@post('/pallets')
def post_pallet():
    response.content_type = 'application/json'
    cookie_name = request.query.cookie

    if not (cookie_name):
        response.status = 400
        return format_response({"error": "Missing parameter"})

    c = conn.cursor()
    c.execute(
        """
        SELECT cookie_name
        FROM cookies
        WHERE cookie_name=?
        """,
        [cookie_name]
    )
    if not (c.fetchone()):
        response.status = 400
        return format_response({"status": "No such cookie"})

    c.execute(
        """
        SELECT  recipe_quantity, quantity, ingredient_name
        FROM    recipeLines
        JOIN    ingredients
        USING   (ingredient_name)
        WHERE   cookie_name =?
        """,
        [cookie_name]
    )
    row = c.fetchone()
    if not (row):
        response.status = 400
        return format_response({"error": "Performance doesnt exist"})

    ingredients = []
    while row is not None:
        ingredients.append(row)
        if (int(row[1]) < int(row[0]) * 54):
            response.status = 400
            return format_response({"status" : "not enough ingredients"})
        row = c.fetchone()
    
    for ingredient in ingredients:
        c.execute(
            """
            UPDATE ingredients
            SET quantity = ?
            WHERE ingredient_name = ?
            """ ,
            [int(ingredient[1]) - (int(ingredient[0]) * 54), ingredient[2]]
        )
    
    c.execute(
        """
        INSERT
        INTO   pallets(cookie_name)
        VALUES (?)
        """,
        [cookie_name]
    )
    conn.commit()
    c.execute(
        """
        SELECT   pallet_id
        FROM     pallets
        WHERE    rowid = last_insert_rowid()
        """
    )
    id = c.fetchone()[0]
    response.status = 200
    return format_response({"status" : "ok" , "id": id})

@get('/pallets')
def get_pallets():
    response.content_type = 'application/json'
    query = ("""
        SELECT  pallet_id, cookie_name, production_date, customer_id, blocked
        FROM    pallets
        LEFT JOIN orders
        USING   (order_id)
        WHERE 1 = 1
        """)
    params = []
    if request.query.after:
        query += "AND production_date > ?"
        params.append(request.query.after)
    if request.query.before:
        query += "AND production_date < ?"
        params.append(request.query.before)
    if request.query.cookie:
        query += "AND cookie_name = ?"
        params.append(request.query.cookie)
    if request.query.blocked:
        query += "AND blocked = ?"
        params.append(request.query.blocked)

    
    c = conn.cursor()
    c.execute(
        query,
        params
    )
    s = [{"id" : pallet_id, "cookie" : cookie_name, "productionDate" : production_date, "customer" : customer_id, "blocked" : bool(blocked)}
         for (pallet_id, cookie_name, production_date, customer_id, blocked) in c]
    response.status = 200
    return format_response({"pallets" : s})

@post('/block/<cookie>/<from_date>/<to_date>')
def post_block(cookie, from_date, to_date):
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        UPDATE pallets
        SET blocked = 1
        WHERE cookie_name = ? AND production_date >= ? AND production_date <= ?
        """,
        [cookie, from_date, to_date]
    )
    conn.commit()
    response.status = 200
    return format_response({"status" : "ok"})

@post('/unblock/<cookie>/<from_date>/<to_date>')
def post_unblock(cookie, from_date, to_date):
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        UPDATE pallets
        SET blocked = 0
        WHERE cookie_name = ? AND production_date >= ? AND production_date <= ?
        """,
        [cookie, from_date, to_date]
    )
    conn.commit()
    response.status = 200
    return format_response({"status": "ok"})


def script_execution(filename):
    with open(filename, 'r') as s:
        sql_script = s.read()
        conn.executescript(sql_script)
    s.closed


run(host=HOST, port=PORT)
