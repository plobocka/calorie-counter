from datetime import datetime, timedelta
from tkinter import *

from Models.user_model import UserModel
from Views.user_view import UserWindow, SetWeightWindow, SetCaloriesIntakeWindow
from Views.user_products_view import AddProductWindow
from Views.user_food_diary_view import AddConsumedProductWindow

DATE_FORMAT = "%Y/%m/%d"


class UserController:
    def __init__(self, root, database_model, user):
        self.master = root
        self.database_model = database_model
        
        self.user_model = UserModel(user, self.database_model)
        self.user_view = UserWindow(root, self.user_model.user)
        
        # set commands on date buttons
        self.user_view.button_prev_date.config(command=self.set_to_prev_day_date)
        #self.user_view.button_set_date.config(command=self.set_to_date)
        self.user_view.button_next_date.config(command=self.set_to_next_day_date)
        self.user_view.button_date_today.config(command=self.set_to_todays_date)

        # set command on set weight button
        self.user_view.button_set_weight.config(command=self.open_set_user_weight_window)
        # set command on set calories intake button
        self.user_view.button_set_calories_intake.config(command=self.open_set_calories_instake_window)

        # set food diary and product tabs as contoller attributes
        self.user_products_view = self.user_view.user_products_view
        self.user_food_diary_view = self.user_view.user_food_diary_view

        self.configure_user_products_view_buttons()
        self.configure_user_food_diary_view_buttons()

    #   DATE
    def set_to_prev_day_date(self):
        curr_date = datetime.strptime(self.user_model.user['current_date'], DATE_FORMAT)
        new_date = curr_date - timedelta(days=1)
        self.set_current_date(format_date(new_date))

    def set_to_date(self):
        pass

    def set_to_next_day_date(self):
        curr_date = datetime.strptime(self.user_model.user['current_date'], DATE_FORMAT)
        new_date = curr_date + timedelta(days=1)
        self.set_current_date(format_date(new_date))

    def set_to_todays_date(self):
        current_date = get_current_date()
        self.set_current_date(current_date)

    def set_current_date(self, new_date):
        self.user_model.set_current_date(new_date)
        self.user_view.update_user_status_view()
        #self.user_products_view.update_products() #but necessary?
        self.user_food_diary_view.update_products() #?

    # WEIGHT
    def open_set_user_weight_window(self):
        self.change_weight_popup = SetWeightWindow(self.master, self.user_model.user['weight']['weight_value'])
        self.change_weight_popup.button_set_weight.config(command=self.set_user_weight)
    
    def set_user_weight(self):
        new_weight = self.change_weight_popup.entry_weight.get()
        current_date = self.user_model.user['current_date']
        current_day_weight = self.database_model.get_user_weight_by_date(self.user_model.user['user_id'],
                                                                            current_date)
        update_weight = False
        if current_day_weight:
            if current_day_weight['weight_value'] != new_weight:
                self.database_model.update_user_weight_on_date(self.user_model.user['user_id'],
                                                               current_date, new_weight)
                update_weight = True
        else:
            self.database_model.insert_weight(self.user_model.user['user_id'], new_weight, current_date)
            update_weight = True

        if update_weight:
            self.user_model.set_current_date(self.user_model.user['current_date'])
            self.user_view.update_weight()
        self.change_weight_popup.destroy()

# CALORIES INTAKE
    def open_set_calories_instake_window(self):
        self.change_calories_intake_popup = SetCaloriesIntakeWindow(self.master, self.user_model.user['calories_to_consume'])
        self.change_calories_intake_popup.button_set_calories_intake.config(command=self.set_user_calories_intake)

    def set_user_calories_intake(self):
        new_calories_intake = self.change_calories_intake_popup.entry_calories_intake.get()
        self.database_model.update_user_calories_intake(self.user_model.user['user_id'], new_calories_intake)
        self.user_model.user['calories_to_consume'] = new_calories_intake
        self.user_model.update_calories_left()
        self.user_view.update_user_status_view()
        self.change_calories_intake_popup.destroy()


# USER PRODUCTS VIEW
    def configure_user_products_view_buttons(self):
        self.user_products_view.button_add_product.config(command=self.open_add_prod_window)
        self.user_products_view.button_delete_product.config(command=self.delete_product)
        self.user_products_view.button_search.config(command=self.search_user_product)


    def search_user_product(self):
        self.user_model.set_current_date(self.user_model.user['current_date'])
        str_to_find = self.user_products_view.entry_search.get()
        self.user_model.update_selected_products_ids(str_to_find)
        self.user_products_view.update_products()
        self.user_view.update_user_status_view()

    def delete_product(self):
        if len(self.user_model.user['selected_products_ids']) > 0:
            prod_index = self.user_products_view.product_selected.get()
            product_id = self.user_model.user['selected_products_ids'][prod_index]
            self.database_model.delete_consumed_product_byID(product_id)
            self.database_model.delete_product_byID(self.user_model.user['user_id'], product_id)

            self.update_consumed_products()
        self.update_products()

    def open_add_prod_window(self):
        self.add_new_product_window = AddProductWindow(self.master)
        self.add_new_product_window.button_add_product.config(command=self.add_product)
        #self.add_new_product_window.button_back.config(command=self.back)

    def add_product(self):
        product_name = self.add_new_product_window.entry_name.get()
        product_calories = self.add_new_product_window.entry_calories.get()

        # errors?
        self.database_model.insert_product(self.user_model.user['user_id'], product_name, product_calories)
        self.update_products()
        self.add_new_product_window.destroy()
        

    def update_products(self):
        self.user_model.set_current_date(self.user_model.user['current_date'])
        str_to_find = self.user_products_view.entry_search.get()
        self.user_model.update_selected_products_ids(str_to_find)
        self.user_products_view.update_products()
        self.user_view.update_user_status_view()

# USER FOOD DIARY VIEW
    def configure_user_food_diary_view_buttons(self):
        self.user_food_diary_view.button_add_product.config(command=self.open_add_consumed_prod_window)
        self.user_food_diary_view.button_delete_cons_product.config(command=self.delete_consumed_product)

    def delete_consumed_product(self):
        if len(self.user_model.user['consumed_products']) > 0:
            index = self.user_food_diary_view.product_selected.get()
            consumed_product_id = self.user_model.user['consumed_products'][index]['consumed_product_id']
            self.database_model.delete_consumed_product_by_userID(self.user_model.user['user_id'], consumed_product_id)
            
            self.update_consumed_products()
        self.update_products()

    def open_add_consumed_prod_window(self):
        self.add_consumed_product_window = AddConsumedProductWindow(self.master, self.user_model.user['products'], self.user_model.user['products_ids'])
        self.add_consumed_product_window.button_add_product.config(command=self.add_consumed_product)
        self.add_consumed_product_window.button_search.config(command=self.search_product)

    def search_product(self):
        str_to_look_for = self.add_consumed_product_window.entry_search.get()
        self.user_model.update_selected_products_ids(str_to_look_for)
        self.add_consumed_product_window.default_radio = 0
        self.add_consumed_product_window.update_products_list(self.user_model.user['selected_products_ids'])

    def add_consumed_product(self):
        if len(self.user_model.user['selected_products_ids']) > 0:
            index = self.add_consumed_product_window.product_selected.get()
            product_id = self.user_model.user['selected_products_ids'][index]
            grammage = self.add_consumed_product_window.entry_grammage.get()

            self.database_model.insert_consumed_product(product_id, self.user_model.user['user_id'], self.user_model.user['current_date'], grammage)

            self.update_consumed_products()
        self.add_consumed_product_window.destroy()
        self.update_products()

    def update_consumed_products(self):
        self.user_model.set_current_date(self.user_model.user['current_date'])
        self.user_food_diary_view.update_products()
        self.user_view.update_user_status_view()


# ----------------------------------------------------
def get_current_date():
        current_date = datetime.now()
        current_date = current_date.strftime(DATE_FORMAT)
        return current_date

def format_date(date):
    date = date.strftime(DATE_FORMAT)
    return date

