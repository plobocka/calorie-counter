from datetime import datetime


class UserModel:
    def __init__(self, user, database_model):
        self.user = user
        self.database_model = database_model

        self.user['weight'] = self.get_user_weight()
        self.user['current_date'] = self.get_current_date()
        self.user['current_date_weight'] = self.get_user_current_date_weight()

        self.user['products_ids'] = []
        self.user['products'] = self.get_user_products()
        self.user['selected_products_ids'] = self.get_user_selected_products_ids()

        self.user['consumed_products'] = self.get_user_consumed_products()
        
        self.user['calories_to_consume'] = self.get_calories_intake()
        self.user['calories_consumed'] = self.get_calories_consumed()
        self.user['calories_left'] = self.get_calories_left()

# GET
    def get_user_current_date_weight(self):
        date = self.user['current_date']
        found_weight = self.database_model.get_first_weight_before_date(self.user['user_id'], date)
        if found_weight is None:
            found_weight = self.database_model.get_first_weight_after_date(self.user['user_id'], date)
        return found_weight

    def get_user_weight_by_date(self):
        date = self.user['current_date']
        return self.database_model.get_user_weight_by_date(self.user['user_id'], date)

    def get_user_weight(self):
        return self.database_model.get_user_weight(self.user['user_id'])

    def get_user_products(self):
        user_products = self.database_model.get_user_products(self.user['user_id'])
        products = {}
        self.user['products_ids'] = []
        for product in user_products:
            products[f'{product["product_id"]}'] = product
            self.user['products_ids'].append(product["product_id"])
        return products

    def get_user_selected_products_ids(self, str_to_look_for=""):
        found_ids = list()
        for prod_id in self.user['products_ids']:
            product_name = self.user['products'][f'{prod_id}']['name']
            str_to_look_for = str_to_look_for.lower()
            product_name = product_name.lower()
            if str_to_look_for in product_name:
                found_ids.append(prod_id)
        return found_ids

    def get_user_consumed_products_at_date(self, date):
        return self.database_model.get_user_consumed_products_by_date(self.user['user_id'], date)

    def get_user_consumed_products(self):
        return self.get_user_consumed_products_at_date(self.user['current_date'])

    def get_calories_intake(self):
        return self.database_model.get_calories_intake(self.user['user_id'])
    
    def get_calories_consumed(self):
        calories_consumed = 0

        # Products calories
        for c_product in self.user['consumed_products']:
            calories_consumed += c_product['calories']
        return calories_consumed

    def get_calories_left(self):
        calories_left = int(self.user['calories_to_consume']) - self.user['calories_consumed']
        if calories_left < 0:
            calories_left = 0
        return calories_left

# UPDATE
    def update_weight(self):
        self.user['weight'] = self.get_user_weight()

    def update_consumed_products(self):
        self.user['consumed_products'] = self.get_user_consumed_products()

    def update_selected_products_ids(self, str_to_look_for):
        self.user['selected_products_ids'] = self.get_user_selected_products_ids(str_to_look_for)

    def update_calories_intake(self):
        self.user['calories_to_consume'] = self.get_calories_intake()

    def update_calories_left(self):
        self.user['calories_left'] = self.get_calories_left()

    # SET CURRENT DATE
    def set_current_date(self, new_date):
        self.user['current_date'] = new_date

        self.user['weight'] = self.get_user_current_date_weight()
        self.user['current_date_weight'] = self.get_user_current_date_weight()
        self.user['products'] = self.get_user_products()

        self.user['consumed_products'] = self.get_user_consumed_products()
        
        self.user['calories_to_consume'] = self.get_calories_intake()
        self.user['calories_consumed'] = self.get_calories_consumed()
        self.user['calories_left'] = self.get_calories_left()


    # GET CURRENT DATE
    def get_current_date(self):
        current_date = datetime.now()
        current_date = current_date.strftime("%Y/%m/%d")
        return current_date

