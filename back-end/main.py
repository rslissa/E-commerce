from database.databaseAPI import DatabaseAPI

if __name__ == '__main__':
    databaseAPI = DatabaseAPI()
    print(databaseAPI.insert_cart_product(2,3))
    databaseAPI.close_connection()

