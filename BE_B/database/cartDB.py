from datetime import date, datetime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj


def create_cart(connection, cursor):
    insert_query = """INSERT INTO public.cart(creation, last_update, buyed, expiring_date,total_items,
    total_unique_items) VALUES (now(), now(), false, now()+ interval '1 day',0,0); """
    cursor.execute(insert_query)
    connection.commit()

    get_query = """Select * from cart where "creation" = ( select max ("creation") from  cart );"""
    cursor.execute(get_query)
    elements = cursor.fetchall()
    elements_serial = []
    if len(elements) == 0:
        return None
    for e in elements[0]:
        elements_serial.append(json_serial(e))
    elements = [tuple(elements_serial)]
    col_names = [desc[0] for desc in cursor.description]

    results = []
    for element in elements:
        el_dict = dict(zip(col_names, element))
        results.append(el_dict)
    if len(results) != 1:
        return False
    result = results[0]
    return result


def list_carts(cursor):
    cursor.execute("SELECT * from public.cart ORDER BY id_cart ASC")
    elements = cursor.fetchall()
    results = []
    for element in elements:
        elements_serial = []
        for e in element:
            elements_serial.append(json_serial(e))
        elements = [tuple(elements_serial)]
        col_names = [desc[0] for desc in cursor.description]
        for element in elements:
            el_dict = dict(zip(col_names, element))
            results.append(el_dict)
    return results


def get_cart(cursor, cart_id):
    query = f"SELECT * from public.cart where id_cart = {cart_id} ORDER BY id_cart ASC"
    cursor.execute(query)
    elements = cursor.fetchall()
    if len(elements) == 0:
        return None
    elements_serial = []
    for e in elements[0]:
        elements_serial.append(json_serial(e))
    elements = [tuple(elements_serial)]
    col_names = [desc[0] for desc in cursor.description]
    results = []
    for element in elements:
        el_dict = dict(zip(col_names, element))
        results.append(el_dict)
    if len(results) != 1:
        return False
    result = results[0]
    return result


def insert_cart_product(connection, cursor, cart_id, product_id, **kwargs):
    insert_query = f""" INSERT INTO public.cart_product (
    id_cart,
    id_product,
    quantity,
    last_update
    ) VALUES (
    '{cart_id}', 
    '{product_id}', 
    {kwargs.get("quantity")},
    '{kwargs.get("last_update")}')"""
    cursor.execute(insert_query)
    connection.commit()


def overwrite_cart_product(connection, cursor, cart_id, product_id, body):
    query = f"""UPDATE public.cart_product SET quantity={body["quantity"]}, last_update='{body["last_update"]}' WHERE 
            id_cart={cart_id} and id_product={product_id}; """
    cursor.execute(query)
    connection.commit()


def insert_cart_by_id(connection, cursor, cart_id, body):
    ret = get_cart(cursor, cart_id)
    query = ""
    print(body)
    if ret is None:
        query = f"""INSERT INTO public.cart(id_cart, creation, last_update, buyed, expiring_date, total_items, 
        total_unique_items, total_price) VALUES ({cart_id}, now(), '{body['last_update']}', False, now(), 
        {body['total_items']}, {body['total_unique_items']}, {body['total_price']}); """
    if ret is not None:
        query = f"""UPDATE public.cart SET last_update='{body['last_update']}', buyed={body['buyed']}, 
        total_items={body['total_items']}, total_unique_items={body['total_unique_items']}, total_price={body['total_price']}
        WHERE id_cart={cart_id};"""
    cursor.execute(query)
    connection.commit()

def update_cart(connection, cursor, operation, cart_id, product_id, new_item, delete, body):
    unique_item = 0
    unique_operation = '+'
    if new_item:
        unique_item = 1
    if delete:
        unique_item = 1
        unique_operation = '-'

    insert_query = f"""
                    UPDATE cart 
                    SET last_update='{body["last_update"]}', total_items = total_items {operation} {body["quantity"]},
                        total_unique_items = total_unique_items {unique_operation} {unique_item},
                        total_price = total_price {operation} (select (product.price*{body["quantity"]})
                                                                 from cart_product 
                                                                 join cart 
                                                                 on cart_product.id_cart = cart.id_cart 
                                                                 join product
                                                                 on cart_product.id_product = product.id_product
                                                                where cart.id_cart = {cart_id} and product.id_product = {product_id}) 
                    WHERE id_cart = {cart_id};
                    """
    print(insert_query)
    cursor.execute(insert_query)
    connection.commit()


def update_cart_product(connection, cursor, operation, cart_id, product_id, body):
    insert_query = f"""
                    UPDATE cart_product
                    SET last_update='{body["last_update"]}', quantity = quantity {operation} {body["quantity"]}
                    WHERE id_cart = {cart_id} and id_product={product_id};
                    """
    cursor.execute(insert_query)
    connection.commit()


def get_cart_table(cursor, timestamp):
    query = f"SELECT * from public.cart where last_update >= '{timestamp}' ORDER BY id_cart ASC"
    cursor.execute(query)
    elements = cursor.fetchall()
    results = []
    for element in elements:
        elements_serial = []
        for e in element:
            elements_serial.append(json_serial(e))
        elements = [tuple(elements_serial)]
        col_names = [desc[0] for desc in cursor.description]
        for element in elements:
            el_dict = dict(zip(col_names, element))
            results.append(el_dict)
    return results


def get_cart_product_table(cursor, timestamp):
    query = f"SELECT * from public.cart_product where last_update >=  '{timestamp}' ORDER BY id_cart, id_product ASC"
    cursor.execute(query)
    elements = cursor.fetchall()
    results = []
    for element in elements:
        elements_serial = []
        for e in element:
            elements_serial.append(json_serial(e))
        elements = [tuple(elements_serial)]
        col_names = [desc[0] for desc in cursor.description]
        for element in elements:
            el_dict = dict(zip(col_names, element))
            results.append(el_dict)
    return results


def get_cart_product(cursor, cart_id, product_id):
    query = f"SELECT * from public.cart_product where id_cart = '{cart_id}' and id_product= '{product_id}' ORDER BY " \
            f"id_cart ASC "
    cursor.execute(query)
    elements = cursor.fetchall()
    if len(elements) == 0:
        return None
    elements_serial = []
    for e in elements[0]:
        elements_serial.append(json_serial(e))
    elements = [tuple(elements_serial)]
    col_names = [desc[0] for desc in cursor.description]
    results = []
    for element in elements:
        el_dict = dict(zip(col_names, element))
        results.append(el_dict)
    if len(results) != 1:
        return False
    result = results[0]
    return result


def remove_cart_product(connection, cursor, cart_id, product_id):
    delete_query = f"Delete from public.cart_product where id_cart = {cart_id} and id_product = {product_id}"
    cursor.execute(delete_query)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record deleted successfully ")
    return count


def remove_cart_products(connection, cursor, cart_id):
    update_query = f"""
                    UPDATE cart 
                    SET total_items = 0,
                        total_unique_items = 0,
                        total_price = 0
                    WHERE id_cart = {cart_id};
                    """
    cursor.execute(update_query)
    connection.commit()

    delete_query = f"Delete from public.cart_product where id_cart = {cart_id}"
    cursor.execute(delete_query)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record deleted successfully ")
    return count

def remove_cart(connection, cursor, cart_id):
    delete_query = f"Delete from public.cart where id_cart = {cart_id}"
    cursor.execute(delete_query)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record deleted successfully ")
    return count