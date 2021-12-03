def get_product_by_id(cursor, idProduct):
    query = f"SELECT * from public.product where id_product = {idProduct} ORDER BY id_product ASC"
    cursor.execute(query)
    elements = cursor.fetchall()
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


def get_product(cursor, name):
    query = f"SELECT * from public.product where name like '{name}' ORDER BY id_product ASC"
    cursor.execute(query)
    elements = cursor.fetchall()
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


def insert_product(connection, cursor, **kwargs):
    insert_query = f""" INSERT INTO product (
    name,
    description,
    price,
    currency_code,
    image_url,
    status,
    stock
    ) VALUES (
    '{kwargs.get("name")}', 
    '{kwargs.get("description")}',
    {kwargs.get("price")},
    '{kwargs.get("currencyCode")}',
    '{kwargs.get("imageURL")}',
    {kwargs.get("status")},
    {kwargs.get("stock")})"""
    cursor.execute(insert_query)
    connection.commit()



def delete_product(connection, cursor, productId):
    delete_query = f"Delete from public.product where id_product = {productId}"
    cursor.execute(delete_query)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record deleted successfully ")
    return count


def list_products(cursor):
    cursor.execute("SELECT * from public.product ORDER BY id_product ASC")
    elements = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    results = []
    for element in elements:
        el_dict = dict(zip(colnames, element))
        results.append(el_dict)
    return results

def list_products_by_cart(cursor, idCart):
    query = f"""select product.*, cart_product.quantity,  (cart_product.quantity*price) as total_product_price
                        from product 
                        join cart_product on product.id_product = cart_product.id_product 
                        where cart_product.id_cart = {idCart}
                        """
    cursor.execute(query)
    elements = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    results = []
    for element in elements:
        el_dict = dict(zip(colnames, element))
        results.append(el_dict)
    print(results)
    return results
