import psycopg2
from psycopg2 import Error
from database import productDB, cartDB, addressDB
from utility import APP_VARIABLES


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

    def get_user_by_email(self, email):
        query = f"select * from public.user where email like '{email}'"
        self.cursor.execute(query)
        elements = self.cursor.fetchall()
        colnames = [desc[0] for desc in self.cursor.description]
        if len(elements) == 0:
            return None
        results = []
        for element in elements:
            el_dict = dict(zip(colnames, element))
            results.append(el_dict)
        if len(results) != 1:
            return False
        user = results[0]
        return user

    def get_product_by_id(self, product_id):
        return productDB.get_product_by_id(self.connection.cursor(), product_id)

    def insert_product(self, **kwargs):
        return productDB.insert_product(self.connection, self.connection.cursor(), **kwargs)

    def list_products(self):
        return productDB.list_products(self.connection.cursor())

    def list_products_by_cart(self, cart_id):
        return productDB.list_products_by_cart(self.connection.cursor(), cart_id)

    def delete_product(self, product_id):
        return productDB.delete_product(self.connection, self.connection.cursor(), product_id)

    def create_cart(self):
        return cartDB.create_cart(self.connection, self.connection.cursor())

    def update_cart(self, new_item, delete, operation, cart_id, product_id, body):
        return cartDB.update_cart(self.connection, self.connection.cursor(), operation, cart_id, product_id, new_item,
                                  delete, body)

    def list_carts(self):
        return cartDB.list_carts(self.connection.cursor())

    def get_cart(self, cart_id):
        return cartDB.get_cart(self.connection.cursor(), cart_id)

    def get_cart_table(self, timestamp):
        return cartDB.get_cart_table(self.connection.cursor(), timestamp)

    def get_cart_product_table(self, timestamp):
        return cartDB.get_cart_product_table(self.connection.cursor(), timestamp)

    def insert_cart_product(self, cart_id, product_id, **kwargs):
        return cartDB.insert_cart_product(self.connection, self.connection.cursor(), cart_id, product_id, **kwargs)

    def overwrite_cart_product(self, cart_id, product_id, body):
        return cartDB.overwrite_cart_product(self.connection, self.connection.cursor(), cart_id, product_id, body)

    def insert_cart_by_id(self, cart_id, body):
        return cartDB.insert_cart_by_id(self.connection, self.connection.cursor(), cart_id, body)

    def get_cart_product(self, cart_id, product_id):
        return cartDB.get_cart_product(self.connection.cursor(), cart_id, product_id)

    def update_cart_product(self, operation, cart_id, product_id, body):
        return cartDB.update_cart_product(self.connection, self.connection.cursor(), operation, cart_id, product_id,
                                          body)

    def remove_cart_product(self, cart_id, product_id):
        return cartDB.remove_cart_product(self.connection, self.connection.cursor(), cart_id, product_id)

    def remove_cart_products(self, cart_id):
        return cartDB.remove_cart_products(self.connection, self.connection.cursor(), cart_id)

    def list_countries(self):
        return addressDB.list_countries(self.connection.cursor())

    def list_sub_countries(self, country_code):
        return addressDB.list_subCountries(self.connection.cursor(), country_code)

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
