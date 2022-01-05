import psycopg2
from psycopg2 import Error
from utility import APP_VARIABLES
from datetime import date, datetime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj


class DatabaseAPI(object):
    def __init__(self):
        try:
            # Connect to an existing database
            self.connection = psycopg2.connect(user=APP_VARIABLES.DB_USER,
                                               password=APP_VARIABLES.DB_PASSWORD,
                                               host=APP_VARIABLES.DB_HOST,
                                               port=APP_VARIABLES.DB_PORT,
                                               database=APP_VARIABLES.DB_NAME)

            # Create a cursor to perform database operations
            self.cursor = self.connection.cursor()
            # Print PostgreSQL details
            print("PostgreSQL server information")
            print(self.connection.get_dsn_parameters(), "\n")
            # Executing a SQL query
            self.cursor.execute("SELECT version();")
            # Fetch result
            record = self.cursor.fetchone()
            print("You are connected to - ", record, "\n")

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def get_cart(self, cart_id):
        cursor = self.connection.cursor()
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

    def create_cart(self):
        cursor = self.connection.cursor()
        insert_query = """INSERT INTO public.cart(creation, last_update, buyed, expiring_date,total_items,
        total_unique_items,total_price) VALUES (now(), now(), false, now()+ interval '1 day',0,0,0); """
        cursor.execute(insert_query)
        self.connection.commit()

    def insert_cart_by_id(self, cart_id, body):
        cursor = self.connection.cursor()
        ret = self.get_cart(cart_id)
        query = ""
        if ret is None:
            query = f"""INSERT INTO public.cart(id_cart, creation, last_update, buyed, expiring_date, total_items, 
            total_unique_items, total_price) VALUES ({cart_id}, now(), '{body['last_update']}', False, now(), 
            {body['total_items']}, {body['total_unique_items']}, {body['total_price']}); """
        if ret is not None:
            query = f"""UPDATE public.cart SET last_update='{body['last_update']}', buyed={body['buyed']}, 
            total_items={body['total_items']}, total_unique_items={body['total_unique_items']}, total_price={body['total_price']}
            WHERE id_cart={cart_id};"""
        cursor.execute(query)
        self.connection.commit()

    def delete_cart(self, id_cart):
        cursor = self.connection.cursor()
        delete_query = f"Delete from public.cart where id_cart = {id_cart}"
        cursor.execute(delete_query)
        self.connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")
        return count

    def get_product_by_id(self, idProduct):
        cursor = self.connection.cursor()
        query = f"SELECT * from public.product where id_product = {idProduct} ORDER BY id_product ASC"
        cursor.execute(query)
        elements = cursor.fetchall()
        if len(elements) == 0:
            return None
        elements_serial = []
        for e in elements[0]:
            elements_serial.append(json_serial(e))
        elements = [tuple(elements_serial)]
        colnames = [desc[0] for desc in cursor.description]
        results = []
        for element in elements:
            el_dict = dict(zip(colnames, element))
            results.append(el_dict)
        if len(results) != 1:
            return False
        result = results[0]
        return result

    def insert_product(self, **kwargs):
        cursor = self.connection.cursor()
        insert_query = f""" INSERT INTO product (
        name,
        description,
        price,
        currency_code,
        image_url,
        status,
        stock,
        last_update
        ) VALUES (
        '{kwargs.get("name")}', 
        '{kwargs.get("description")}',
        {kwargs.get("price")},
        '{kwargs.get("currency_code")}',
        '{kwargs.get("imageURL")}',
        {kwargs.get("status")},
        {kwargs.get("stock")},
        '{kwargs.get("last_update")}')"""
        cursor.execute(insert_query)
        self.connection.commit()

    def get_cart_product(self, cart_id, product_id):
        cursor = self.connection.cursor()
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

    def insert_cart_product(self, cart_id, product_id, **kwargs):
        cursor = self.connection.cursor()
        insert_query = f""" INSERT INTO public.cart_product (
        id_cart,
        id_product,
        quantity,
        last_update, 
        cancelled
        ) VALUES (
        '{cart_id}', 
        '{product_id}', 
        {kwargs.get("quantity")},
        '{kwargs.get("last_update")}',
        {kwargs.get("cancelled")})"""
        cursor.execute(insert_query)
        self.connection.commit()


