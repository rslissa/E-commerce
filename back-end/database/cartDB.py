from datetime import date, datetime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj


def create_cart(connection, cursor):
    insert_query = """INSERT INTO public.cart(creation, last_update, buyed, expiring_date) VALUES (now(), now(), 
    false, now()+ interval '1 day'); """
    cursor.execute(insert_query)
    connection.commit()

    get_query = """Select * from cart where "creation" = ( select max ("creation") from  cart );"""
    cursor.execute(get_query)
    elements = cursor.fetchall()
    elements_serial = []
    for e in elements[0]:
        elements_serial.append(json_serial(e))
    elements = []
    elements.append(tuple(elements_serial))
    colnames = [desc[0] for desc in cursor.description]
    if len(elements) == 0:
        return None
    results = []
    for element in elements:
        el_dict = dict(zip(colnames, element))
        results.append(el_dict)
    if len(results) != 1:
        return False
    result = results[0]
    return result


def get_cart(cursor, idCart):
    query = f"SELECT * from public.cart where id_cart = {idCart} ORDER BY id_cart ASC"
    cursor.execute(query)
    elements = cursor.fetchall()
    elements_serial = []
    for e in elements[0]:
        elements_serial.append(json_serial(e))
    elements = []
    elements.append(tuple(elements_serial))
    colnames = [desc[0] for desc in cursor.description]
    if len(elements) == 0:
        return None
    results = []
    for element in elements:
        el_dict = dict(zip(colnames, element))
        results.append(el_dict)
    if len(results) != 1:
        return False
    result = results[0]
    return result


def insert_cart_product(connection, cursor, idCart, idProduct, **kwargs):
    insert_query = f""" INSERT INTO public.cart_product (
    id_cart,
    id_product,
    quantity
    ) VALUES (
    '{idCart}', 
    '{idProduct}', 
    {kwargs.get("quantity")})"""
    cursor.execute(insert_query)
    connection.commit()


def update_cart(connection, cursor, idCart, newItem, **kwargs):
    unique_item = 0
    if newItem == True:
        unique_item = 1
    insert_query = f"""
                    UPDATE cart 
                    SET total_items = total_items + {kwargs.get("quantity")},
                        total_unique_items = total_unique_items + {unique_item}
                    WHERE id_cart = '{idCart}';
                    """
    cursor.execute(insert_query)
    connection.commit()

def update_cart_product(connection, cursor, idCart, idProduct, **kwargs):
    insert_query = f"""
                    UPDATE cart_product
                    SET quantity = quantity + {kwargs.get("quantity")}
                    WHERE id_cart = {idCart} and id_product={idProduct};
                    """
    cursor.execute(insert_query)
    connection.commit()


def get_cart_product(cursor, idCart, idProduct):
    query = f"SELECT * from public.cart_product where id_cart = '{idCart}' and id_product= '{idProduct}' ORDER BY id_cart ASC"
    cursor.execute(query)
    elements = cursor.fetchall()
    if len(elements) == 0:
        return None
    elements_serial = []
    for e in elements[0]:
        elements_serial.append(json_serial(e))
    elements = [tuple(elements_serial)]
    colnames = [desc[0] for desc in cursor.description]
    if len(elements) == 0:
        return None
    results = []
    for element in elements:
        el_dict = dict(zip(colnames, element))
        results.append(el_dict)
    if len(results) != 1:
        return False
    result = results[0]
    return result
