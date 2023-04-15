from Database import database
import csv
import os.path

class DataBaseModel:
    def __init__(self):
        if not os.path.isfile("database.db"):
            self.create_tables()
        self.connection = database.connect_to_db()

    def create_tables(self):
        database.create_tables()

    # INSERT
    def insert_user(self, login, password, email, calories_intake):
        database.insert_user(login, password, email, calories_intake)

        with open('products.csv', 'r') as read_obj:
            csv_reader = csv.reader(read_obj, delimiter=';')
            list_of_csv = list(map(tuple, csv_reader))
        for product in list_of_csv:
            self.insert_product(self.get_user_by_login(login)['user_id'], product[0], product[1])


    def insert_product(self, id_user, product_name, calories):
        database.insert_product(id_user, product_name, calories)

    def insert_weight(self, id_user, weight_value, weight_date):
        database.insert_weight(id_user, weight_value, weight_date)

    def insert_consumed_product(self, id_product, id_user, consumption_date, grammage):
        database.insert_consumed_product(id_product, id_user, consumption_date, grammage)

    # GET
    def get_user_by_login(self, login):
        row = database.get_user_by_login(login)
        return self.user_row_to_dictonary(row)

    def get_user_by_login_and_password(self, login, password):
        row = database.get_user_by_login_and_password(login, password)
        user = self.user_row_to_dictonary(row)
        return user

    def get_user_weight(self, user_id):
        row = database.get_user_weight(user_id)
        return self.weight_row_to_dictonary(row)

    def get_user_products(self, user_id):
        rows = database.get_user_products(user_id)

        products = list()

        for row in rows:
            product = self.product_row_to_dictonary(row)
            products.append(product)

        return products

    def get_calories_intake(self, user_id):
        row = database.get_user_calories_intake(user_id)
        calories_intake = row[0]
        return  calories_intake

    def get_user_consumed_products_by_date(self, user_id, current_date):
        rows = database.get_user_consumed_products_by_date(user_id, current_date)
        
        consumed_products = list()

        for row in rows:
            cons_product = self.consumed_product_row_to_dictonary(row)
            cons_product['calories'] = int(float(cons_product['calories']) / 100 * cons_product['grammage'])
            consumed_products.append(cons_product)

        return consumed_products

    # get weight
    def get_user_weight(self, user_id):
        row = database.get_user_weight(user_id)
        return self.weight_row_to_dictonary(row)

    def get_first_weight_before_date(self, user_id, current_date):
        row = database.get_first_weight_before_date(user_id, current_date)
        return self.weight_row_to_dictonary(row)

    def get_first_weight_after_date(self, user_id, current_date):
        row = database.get_first_weight_after_date(user_id, current_date)
        return self.weight_row_to_dictonary(row)

    def get_user_weight_by_date(self, user_id, date):
        row = database.get_user_weight_by_date(user_id, date)
        return self.weight_row_to_dictonary(row)

    # UPDATE
    def update_user_weight_on_date(self, user_id, weight, date):
        database.update_user_weight_date(user_id, weight, date)

    def update_product(self, product_id,  product_name, calories):
        database.update_product(product_id, product_name, calories)

    def update_consumed_product(self, consumed_product_id, grammage):
        database.update_consumed_product(consumed_product_id, grammage)

    def update_user_calories_intake(self, user_id, calories_intake):
        database.update_calories_intake(calories_intake, user_id)

    # DELETE
    def delete_product_byID(self, user_id, product_id):
        database.delete_product(product_id, user_id)

    def delete_consumed_product_byID(self, consumed_product_id):
        database.delete_consumed_product_by_id(consumed_product_id)

    def delete_consumed_product_by_userID(self, user_id, consumed_product_id):
        database.delete_consumed_product_user_id(user_id, consumed_product_id)

    # OTHERS
    @staticmethod
    def user_row_to_dictonary(row):
        if row is not None:
            user = {
                'user_id': row[0],
                'login': row[1],
                'password': row[2],
                'email': row[3],
                'calories_intake': row[4]
            }
            return user
        else:
            return None

    @staticmethod
    def weight_row_to_dictonary(row):
        if row is not None:
            weight = {
                'weight_id': row[0],
                'user_id': row[1],
                'weight_value': row[2],
                'weight_date': row[3]
            }
            return weight
        else:
            return None

    @staticmethod
    def product_row_to_dictonary(row):
        if row is not None:
            product = {
                'product_id': row[0],
                'user_id': row[1],
                'name': row[2],
                'calories': row[3]
            }
            return product
        else:
            return None

    @staticmethod
    def consumed_product_row_to_dictonary(row):
        if row is not None:
            consumed_product = {
                'consumed_product_id': row[0],
                'product_id': row[1],
                'user_id': row[2],
                'consumption_date': row[3],
                'grammage': row[4],
                'name': row[5],
                'calories': row[6]
            }
            return consumed_product
        else:
            return None
            