import psycopg2
from psycopg2 import Error
from database import productDB, cartDB, addressDB


class DatabaseAPI(object):
    def __init__(self):
        try:
            # Connect to an existing database
            self.connection = psycopg2.connect(user="postgres",
                                               password="postgres",
                                               host="127.0.0.1",
                                               port="5432",
                                               database="ecommerce")

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

    def get_product(self, name):
        return productDB.get_product(self.connection.cursor(), name)

    def get_product_by_id(self, idProduct):
        return productDB.get_product_by_id(self.connection.cursor(), idProduct)

    def insert_product(self, name, **kwargs):
        return productDB.insert_product(self.connection, self.connection.cursor(), name, **kwargs)

    def list_products(self):
        return productDB.list_products(self.connection.cursor())

    def list_products_by_cart(self, idCart):
        return productDB.list_products_by_cart(self.connection.cursor(),idCart)

    def delete_product(self, name):
        return productDB.delete_product(self.connection, self.connection.cursor(), name)

    def create_cart(self):
        return cartDB.create_cart(self.connection, self.connection.cursor())

    def update_cart(self,newItem, delete, operation, idCart, idProduct, body):
        return cartDB.update_cart(self.connection, self.connection.cursor(), operation, idCart, idProduct, newItem,delete, body)

    def get_cart(self, idCart):
        return cartDB.get_cart(self.connection.cursor(), idCart)

    def insert_cart_product(self, idCart, idProduct, **kwargs):
        return cartDB.insert_cart_product(self.connection, self.connection.cursor(), idCart, idProduct, **kwargs)

    def get_cart_product(self, idCart, idProduct):
        return cartDB.get_cart_product(self.connection.cursor(), idCart, idProduct)

    def update_cart_product(self, operation, idCart, idProduct, body):
        return cartDB.update_cart_product(self.connection, self.connection.cursor(), operation, idCart, idProduct,
                                          body)
    def remove_cart_product(self, idCart, idProduct):
        return cartDB.remove_cart_product(self.connection, self.connection.cursor(), idCart, idProduct)

    def remove_cart_products(self, idCart):
        return cartDB.remove_cart_products(self.connection, self.connection.cursor(), idCart)

    def list_countries(self):
        return addressDB.list_countries(self.connection.cursor())

    def list_subCountries(self, countryCode):
        return addressDB.list_subCountries(self.connection.cursor(),countryCode)
    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
